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
	
def main():
	#runCommand("rm log")	# Clear log

	# Set device
	device_name = "nano328"
	#device_name = ""
	
	# Set Serial port
	serial_port = "/dev/ttyUSB0"
	#serial_port = "/dev/ttyACM0"
	
	#runCommand("./ino_cmds.sh -b -u -m nano328 -p /dev/ttyUSB0")

	INITIAL_AMOUNT_CHILI_TOP = 200
	INITIAL_AMOUNT_CHILI_BOT = 200
	PUMP_CHILI_TOP = 0
	PUMP_CHILI_BOT = 1

	# Connect to serial
	waterSystem = water(serial_port)

	# Water bottom
	waterSystem.autoWater(PUMP_CHILI_BOT,INITIAL_AMOUNT_CHILI_BOT)

	sleep(20.0)	
	
	# Water top
	waterSystem.autoWater(PUMP_CHILI_TOP,INITIAL_AMOUNT_CHILI_TOP)	

	sleep(20.0)
		
	quit()
	
if __name__ == '__main__':
    main()

