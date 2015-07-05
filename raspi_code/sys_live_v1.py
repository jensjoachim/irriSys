

# Wish list
# Somehow lock arduino after ERROR
# Make safe on start serial
# Echo message
# git



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
	runCommand("rm log")	# Clear log

	# Set device
	device_name = "nano328"
	#device_name = ""
	
	# Set Serial port
	serial_port = "/dev/ttyUSB0"
	#serial_port = "/dev/ttyACM0"
	
	#runCommand("./ino_cmds.sh -b -u -m nano328 -p /dev/ttyUSB0")

	WATER_HOUR = 22 #11;
	WATER_AMOUNT = 500 
	
	while 1:
		if getHour() == WATER_HOUR:
			# Connect to serial
			waterSystem = water(serial_port)
			# Water
			waterSystem.waterIn(300)
			# Send water to plant
			waterSystem.waterTo(0,60)
			# Wait an hour
			while getHour() == WATER_HOUR:
				sleep(60.0)
			sleep(60.0)
		
	quit()
	
if __name__ == '__main__':
    main()

