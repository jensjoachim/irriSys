
#include "hx711.h"
#include <Servo.h> 

// Servo
Servo servo_0;  // create servo object to control a servo 
byte servo_pos_0 = 73;
#define servo_pin_0 9

// Amp/Scale
#define amp_pin_slk A1
#define amp_pin_dout A0

// Timeout
long tic;
long timeout_delay = 2000; //1000;

// Motor control
// Right pump (back)
#define motor_pin_0 3		
byte motor_speed_0 = 0;		
unsigned long motor_stop_0 = 0;
unsigned long motor_run_0 = 20*1000; // 20sek
// Left pump (back)
#define motor_pin_1 5		
byte motor_speed_1 = 0;		
unsigned long motor_stop_1 = 0;
unsigned long motor_run_1 = 5*1000; // 5sek
// Left pump (front)
#define motor_pin_2 6		
byte motor_speed_2 = 0;		
unsigned long motor_stop_2 = 0;
unsigned long motor_run_2 = 5*1000; // 5sek
// Left botttom (front)
#define motor_pin_3 10		
byte motor_speed_3 = 0;		
unsigned long motor_stop_3 = 0;
unsigned long motor_run_3 = 5*1000; // 5sek


// Commands
#define SET_SERVO_0 	0x00	// 4 * Servos
#define GET_SERVO_0		0x04

#define GET_SCALE_0		0x08	// 4 * Scales

#define SET_MOTOR_0		0x10	// 8 * Motors
#define SET_MOTOR_1		0x11
#define SET_MOTOR_2		0x12
#define SET_MOTOR_3		0x13
#define GET_MOTOR_0		0x18	
#define GET_MOTOR_1		0x19
#define GET_MOTOR_2		0x1A	
#define GET_MOTOR_3		0x1B

#define TEST_0			0x80	// 16 * Tests
#define TEST_1			0x81	

void setup()
{
	// Serial 
	Serial.begin(9600); 	// Init serial connection
	
	// Servo
	servo_0.attach(servo_pin_0);		// Init servo motor
	setServo(servo_pos_0);
	
	// Amp
	pinMode(amp_pin_slk, OUTPUT);
	pinMode(amp_pin_dout, INPUT);
	digitalWrite(amp_pin_slk, HIGH);
	delayMicroseconds(100);
	digitalWrite(amp_pin_slk, LOW);
	
	// Motors
	pinMode(motor_pin_0, OUTPUT);
	analogWrite(motor_pin_0,motor_speed_0);
	motor_stop_0 = motor_run_0 + millis();
	
	pinMode(motor_pin_1, OUTPUT);
	analogWrite(motor_pin_1,motor_speed_1);	
	motor_stop_1 = motor_run_1 + millis();
	
	pinMode(motor_pin_2, OUTPUT);
	analogWrite(motor_pin_2,motor_speed_2);	
	motor_stop_2 = motor_run_2 + millis();
	
	pinMode(motor_pin_3, OUTPUT);
	analogWrite(motor_pin_3,motor_speed_3);	
	motor_stop_3 = motor_run_3 + millis();
}

void loop()
{	
	// Check for incoming bytes
	if (Serial.available()) {
		byte incomingByte = Serial.read();
		switch (incomingByte) {
			case SET_SERVO_0:
				if (timeoutM() == 0) {break;}
				setServo(Serial.read());
				break;
			case GET_SERVO_0:
				getServo();	
				break;	
			case GET_SCALE_0:
				sendScaleValue();
				break;
			case SET_MOTOR_0:
				if (timeoutM() == 0) {break;}
				setMotorSpeed(Serial.read(),0);
				break;
			case SET_MOTOR_1:
				if (timeoutM() == 0) {break;}
				setMotorSpeed(Serial.read(),1);
				break;
			case SET_MOTOR_2:
				if (timeoutM() == 0) {break;}
				setMotorSpeed(Serial.read(),2);
				break;	
			case SET_MOTOR_3:
				if (timeoutM() == 0) {break;}
				setMotorSpeed(Serial.read(),3);
				break;	
			case GET_MOTOR_0:
				getMotorSpeed(0);
				break;
			case GET_MOTOR_1:
				getMotorSpeed(1);	
				break;
			case GET_MOTOR_2:
				getMotorSpeed(2);	
				break;		
			case GET_MOTOR_3:
				getMotorSpeed(3);	
				break;					
			case TEST_0:
				Serial.write(10);
				break;	
			case TEST_1:
				Serial.write(11);
				break;			
			default: 
				break;
		}
	}	

	// Check if motor has to be stopped
	if (millis() > motor_stop_0) {
		setMotorSpeed(0,0);
	}
	if (millis() > motor_stop_1) {
		setMotorSpeed(0,1);
	}
	if (millis() > motor_stop_2) {
		setMotorSpeed(0,2);
	}
	if (millis() > motor_stop_3) {
		setMotorSpeed(0,3);
	}
}

byte timeoutM() {
	tic = millis() + timeout_delay; // save time
	while (!Serial.available()) {
		if (tic < millis()) {
			return 0;
		}
	}
	return 1;
}


void setServo(byte pos) {
	servo_0.write(pos); 
	servo_pos_0 = pos;
}

void getServo() {
	Serial.write(servo_pos_0);
}


void setMotorSpeed(byte k, byte n) {
	switch (n) {
		case 0:
			motor_speed_0 = k;
			analogWrite(motor_pin_0, motor_speed_0);
			motor_stop_0 = motor_run_0 + millis();
			break;
		case 1:
			motor_speed_1 = k;
			analogWrite(motor_pin_1, motor_speed_1);
			motor_stop_1 = motor_run_1 + millis();
			break;	
		case 2:
			motor_speed_2 = k;
			analogWrite(motor_pin_2, motor_speed_2);
			motor_stop_2 = motor_run_2 + millis();
			break;	
		case 3:
			motor_speed_3 = k;
			analogWrite(motor_pin_3, motor_speed_3);
			motor_stop_3 = motor_run_3 + millis();
			break;				
		default: 
			break;
	}			
}

void getMotorSpeed(byte n) {
	switch (n) {
		case 0:
			Serial.write(motor_speed_0);
			break;
		case 1:
			Serial.write(motor_speed_1);
			break;
		case 2:
			Serial.write(motor_speed_2);
			break;
		case 3:
			Serial.write(motor_speed_3);
			break;			
		default: 
			break;
	}			
}

void sendScaleValue() {
	byte data[3];

	while (digitalRead(amp_pin_dout));

	for (byte j = 0; j < 3; j++)
	{
		for (byte i = 0; i < 8; i++)
		{
			digitalWrite(amp_pin_slk, HIGH);
			bitWrite(data[2 - j], 7 - i, digitalRead(amp_pin_dout));
			digitalWrite(amp_pin_slk, LOW);
		}
	}
 
	digitalWrite(amp_pin_slk, HIGH);
	digitalWrite(amp_pin_slk, LOW);
  
	Serial.write(data[2]); 
	Serial.write(data[1]); 
	Serial.write(data[0]); 
}
