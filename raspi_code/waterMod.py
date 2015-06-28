
import os
import subprocess
import serial
from time 		import sleep, gmtime, strftime 
import math
import time
import inspect

from waterSerial import *
import waterLog

class water:

	def __init__(self,port_s):

		# Commands
		self.CMD_SET_SERVO = int("0x00", 0)		# 4 * Servos
		self.CMD_GET_SERVO = int("0x04", 0)

		self.CMD_GET_SCALE = int("0x08", 0)		# 4 * Scales

		self.CMD_SET_MOTOR_0 = int("0x10", 0)	# 8 * Motors
		self.CMD_SET_MOTOR_1 = int("0x11", 0)
		self.CMD_GET_MOTOR_0 = int("0x18", 0)
		self.CMD_GET_MOTOR_1 = int("0x19", 0)

		self.CMD_TEST_0 = int("0x80", 0)			# 16 * Tests
		self.CMD_TEST_1 = int("0x81", 0)	

		# SERIAL
		self.SERIAL_TIMEOUT_MS = 50

		# SCALE	
		self.SCALE_OFFSET = -82.025
		self.SCALE_AMP = 48.977

		# SERVO
		self.SERVO_LEFT_DEG = 153
		self.SERVO_RIGHT_DEG = 1
		self.SERVO_MIDDLE_DEG = 77
		self.SERVO_SPEED_UP = 0
		self.SERVO_SPEED_DOWN = 0.02

		# WATER
		self.WATER_BUCKET_MAX = 200
		self.WATER_FILL_BUCKET_TIME = 30
		
		ws = waterSerial(port_s)
		self.port = ws.getPort()
		
		#### WAIT FOR ARDUINO ####
		sleep(3.0)

	


	def runCommand(self,command):
		p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		waterLog.log("",output)	
		if err:
			waterLog.log("E",output)	
		return output

	def getCurrentTimeMS(self):
		return long(time.time()*1000)

	def checkTOMS(self,k):
		if k < self.getCurrentTimeMS():
			waterLog.log("E","Time Out")

	# def log(self, s0, s1):
		# # s0 = "E" 			<- Log error and EXIT
		# # s0 = "I"			<- Log and print message
		# # s0 = ""			<- Log method
		# # s1 = "Hej hej"	<- Message
		# if s0 == "E":
			# output = "ERROR: " + strftime("%d %b %Y %H:%M:%S", gmtime()) + " " + inspect.stack()[1][3] + "() " + s1 + "\n"
			# file = open("log", "a")
			# file.write(output)
			# print output # Print message in terminal
			# i = 1
			# s = ""
			# # trace back
			# while inspect.stack()[i][3] != "main":
				# s = s + "\n" + inspect.stack()[i][3] + "() "
				# i = i + 1
				
			# s = s + "\n" + inspect.stack()[i][3] + "() "	
			# print s
			# file = open("log", "a")
			# file.write(s)
			# quit()	# And quit
		# elif s0 == "I":	
			# msg = strftime("%d %b %Y %H:%M:%S", gmtime()) + " INFO: "+ s1 + "\n"
			# file = open("log", "a")
			# file.write(msg)
			# print s1
		# else:
			# output = strftime("%d %b %Y %H:%M:%S", gmtime()) + " " + inspect.stack()[1][3] + "() " + s1 + "\n"
			# file = open("log", "a")
			# file.write(output)
		
		
	# def build(self,device_name): 
		# s = "ino build -m "+device_name
		# waterLog.log("I","Building with: "+s)
		# if self.runCommand(s).find("failed") != -1:
			# waterLog.log("E","FAILED!")
		# waterLog.log("I","Build success!")		

	# def upload(self,device_name,serial_port):
		# s = "ino upload -m "+device_name+" -p "+serial_port
		# waterLog.log("I","Uploading with: "+s)
		# if self.runCommand(s).find("FAILED") != -1:
			# waterLog.log("E","FAILED!")
		# waterLog.log("I","Upload success!")	

		
	def serialReadBytes(self, cmd, n):
		self.port.flushInput() 			# flush input buffer to avid junk
		self.port.write(chr(cmd))	# Send Command
		tic = int(time.time()*100) + self.SERIAL_TIMEOUT_MS
		x = 0
		d = 0
		if n > 0:
			while tic > int(time.time()*100):
				if self.port.inWaiting() > 0:
					x = (x << 8) | ord(self.port.read(1))
					d = d + 1
					if d == n:	# Tjek all bytes received
						break
					
		mes = "Read %i of %i bytes" % (d, n)
		if d != n: # Tjek that all byte have been recieved
			waterLog.log("E",mes)
			
		#log("",mes)	
		return x				

	def scaleRead(self):
		x = self.serialReadBytes(self.CMD_GET_SCALE, 3)
		# Sign extend	
		if x & 8388608 != 0:
			x = x | (-16777216)	
		return int(x)		

	def scaleReadCont(self,n):
		x = 0.0
		for g in range(0, n):
			x = self.scaleRead() * 0.01 + x	
			
		x = x/n		
		return x	

	# def scaleCalibrate(port,n):	
	# print "Hands off!"
	# m1 = scaleReadCont(port,25)

	# print "Put on object"
	# k = 10
	# while k > 0:
		# sleep(1.0)
		# k = k - 1
		# print "Wait %i sec" % k
		
	# m2 = scaleReadCont(port,25)
	# print "m1: %.3f, m2: %.3f" % (m1, m2)
	# offset = m1
	# amp = (m2 - m1) / n
	# print "Offset: %.3f, Amp: %.3f" % (offset, amp)

	def scaleReadTrue(self,n):
		x = self.scaleReadCont(n)	
		x = (x - self.SCALE_OFFSET) / self.SCALE_AMP
		x = round(x,1)	
		if x < -100.0 or x > 500:
			mes = "Value = %i" % n
			waterLog.log("E",mes)

		mes = "n = %i" % x	
		waterLog.log("",mes)
		return x	
		
	# def scaleZero(port):
	# global SCALE_OFFSET   
	# SCALE_OFFSET = scaleReadCont(port,25)
	
	def servoSet(self,n):	
		self.serialReadBytes(self.CMD_SET_SERVO,0)
		self.serialReadBytes(n,0)	
	
	

	def servoGet(self):
		return self.serialReadBytes(self.CMD_GET_SERVO,1)

	def servoUse(self,n):
		self.servoSet(n)
		x = self.servoGet()
		if x != n:
			mes = "Aim: %i, Real: %i" % (n,x)
			waterLog.log("E",mes)
		
	def servoUp(self):
		waterLog.log("","")
		self.servoUse(self.SERVO_MIDDLE_DEG)
		
	def servoLeft(self):
		Bucketlog("","")
		for i in range(self.SERVO_MIDDLE_DEG,self.SERVO_LEFT_DEG+1):	
			self.servoSet(i)
			sleep(self.SERVO_SPEED_DOWN)
			
		self.servoUse(self.SERVO_LEFT_DEG)	
		
	def servoRight(self):	
		waterLog.log("","")
		for i in range(self.SERVO_RIGHT_DEG,self.SERVO_MIDDLE_DEG):
			self.servoSet(self.SERVO_MIDDLE_DEG-i)
			sleep(self.SERVO_SPEED_DOWN)
			
		self.servoUse(self.SERVO_MIDDLE_DEG-i)			
		
	def usePump(self,k):
		msg = "Value k = %i" % k
		waterLog.log("",msg)
		if k < 0 and k > 255:
			msg = "%i < 0 and %i > 255" % (k,k)
			waterLog.log("E",msg)	

		self.serialReadBytes(self.CMD_SET_MOTOR_0,0)
		self.serialReadBytes(k,0)

		x = self.serialReadBytes(self.CMD_GET_MOTOR_0,1)
		if x != k:
			msg = "Aim: %i, Real: %i" % (k,x)
			waterLog.log("E",msg)	
		
	def waterIn(self,k):
		mean_n = 10;
		m_speed = 255;
		# Calculate number of buckets and rest
		b_n = k / self.WATER_BUCKET_MAX
		rest = k
		msg = "Weighting of %iml in %i buckets." %(k,b_n+1)
		waterLog.log("","")
		waterLog.log("I",msg)
		print "b_n: %i, rest: %i" % (b_n,rest) # Print something here
		# Weight: b_n
		w_TO = (b_n + 1) * self.WATER_FILL_BUCKET_TIME * 1000 + self.getCurrentTimeMS()# Set TO
		sum = 0
		if not(rest > self.WATER_BUCKET_MAX):	# If no full buckets are used
			empty = self.scaleReadTrue(mean_n)
			
		while rest > self.WATER_BUCKET_MAX:		# Weight full buckets
			self.checkTOMS(w_TO) # Check Time Out
			waterLog.log("I","Setting Bucket Up")
			self.servoUp()
			msg = "Filling bucket to: %iml" % self.WATER_BUCKET_MAX
			waterLog.log("I",msg)
			self.usePump(m_speed)	# Start pump
			x = 0
			b_TO = self.WATER_FILL_BUCKET_TIME * 1000 + self.getCurrentTimeMS()# Set TO
			while x < self.WATER_BUCKET_MAX:
				self.checkTOMS(w_TO) # Check Time Out
				self.checkTOMS(b_TO) # Check Time Out
				x = self.scaleReadTrue(1)

			self.usePump(0)	# Stop pump
			sleep(1.0)
			filled = self.scaleReadTrue(mean_n)
			waterLog.log("I","Setting Bucket Right")
			self.servoRight()
			sleep(2.0)
			self.servoUp()
			sleep(1.0)	
			empty = self.scaleReadTrue(mean_n)
			sum = sum + filled-empty
			rest = rest - (filled-empty)
			msg = "Filled: %.1f, Empty: %.1f, Bucket: %.1f, Rest: %i, Sum: %.1f" % (filled,empty,filled-empty,rest,sum)
			waterLog.log("I",msg)

		# Weight: rest
		waterLog.log("I","Setting Bucket Up")
		self.servoUp()
		msg = "Filling bucket to: %iml" % rest
		waterLog.log("I",msg)
		self.usePump(m_speed)	# Start pump
		x = empty
		b_TO = self.WATER_FILL_BUCKET_TIME * 1000 + self.getCurrentTimeMS()# Set TO
		while (x - empty) < rest:
			self.checkTOMS(w_TO) # Check Time Out
			self.checkTOMS(b_TO) # Check Time Out		
			x = self.scaleReadTrue(1)	

		self.usePump(0)	# Stop pump
		sleep(1.0)
		filled = self.scaleReadTrue(mean_n)
		sum = sum + (filled-empty)
		rest = rest - (filled-empty)
		msg = "Filled: %.1f, Empty: %.1f, Bucket: %.1f, Rest: %i, Sum: %.1f" % (filled,empty,filled-empty,rest,sum)
		waterLog.log("I",msg)
		waterLog.log("I","Setting Bucket Right")
		self.servoRight()
		sleep(2.0)
		self.servoUp()

		return sum
			