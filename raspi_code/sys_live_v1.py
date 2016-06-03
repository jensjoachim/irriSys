import os
import subprocess

from waterSerial import *
from waterMod import *

from time 		import gmtime, strftime 

def runCommand(command):
	p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	print "OUTPUT: " + output	
	if err:
		print "ERROR: " + output
		quit()		
	return output
	
def getHour():
	return (int(strftime("%H ", gmtime())) + 2) % 24

def main():
	#runCommand("rm log")	# Clear log

	# Set device
	device_name = "nano328"
	#device_name = ""
	
	# Set Serial port
	serial_port = "/dev/ttyUSB0"
	#serial_port = "/dev/ttyACM0"
	
	#runCommand("./ino_cmds.sh -b -u -m nano328 -p /dev/ttyUSB0")

	AMOUNT_CHILI_TOP = 400
	AMOUNT_CHILI_BOT = 400
	PUMP_TIME_CHILI_TOP = 60
	PUMP_TIME_CHILI_BOT = 60
	PUMP_CHILI_TOP = 0
	PUMP_CHILI_BOT = 1

	#waterSystem = water(serial_port)
	#waterSystem.servoLeft()
	#sleep(1.0)
	#waterSystem.servoUp()
	#sleep(1.0)
	#waterSystem.waterOut()
	#waterSystem.servoUp()
	#waterSystem.usePumpOut(255)
	#sleep(15.0)
	#waterSystem.usePumpOut(0)
	#waterSystem.servoLeft()
	#sleep(5.0)
	#waterSystem.servoUp()
 	#quit() 
	

	# Connect to serial
	waterSystem = water(serial_port)	
	# Water PUMP_CHILI_TOP
	waterSystem.waterIn(AMOUNT_CHILI_BOT)
	waterSystem.waterTo(PUMP_CHILI_BOT,PUMP_TIME_CHILI_BOT)
	sleep(60.0*2)
	waterSystem.waterOut()
	# Water PUMP_CHILI_TOP
	waterSystem.waterIn(AMOUNT_CHILI_TOP)
	waterSystem.waterTo(PUMP_CHILI_TOP,PUMP_TIME_CHILI_TOP)
	sleep(60.0*2)
	waterSystem.waterOut()

	sleep(60.0)
		
	quit()
	
if __name__ == '__main__':
    main()

