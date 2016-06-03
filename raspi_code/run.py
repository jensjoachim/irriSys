

# Wish list
# Somehow lock arduino after ERROR
# Make safe on start serial
# Echo message
# git



import os
import subprocess

from waterSerial import *
from waterMod import *

def runCommand(command):
	p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	print "OUTPUT: " + output	
	if err:
		print "ERROR: " + output
		quit()		
	return output

def build(device_name): 
	s = "ino build -m "+device_name
	print "Building with: " + s
	if runCommand(s).find("failed") != -1:
		print "Build FAILED!"
		quit()
	print "Build success!"	

def upload(device_name,serial_port):
	s = "ino upload -m "+device_name+" -p "+serial_port
	print "Uploading with: "+s
	if runCommand(s).find("FAILED") != -1:
		print "Upload FAILED!"
		quit()
	print "Upload success!"

def main():
	#runCommand("rm log")	# Clear log

	# Set device
	device_name = "nano328"
	#device_name = ""
	
	# Set Serial port
	serial_port = "/dev/ttyUSB0"
	#serial_port = "/dev/ttyACM0"
	
	runCommand("./ino_cmds.sh -b -u -m nano328 -p /dev/ttyUSB0")

	waterSystem = water(serial_port)
	waterSystem.waterIn(200)
	waterSystem.waterTo(0,30)
	waterSystem.waterIn(200)
	waterSystem.waterTo(1,30)
	quit()
	
	#while 1:
	#	print waterSystem.scaleReadCont(2)
		
	while 1:
		sleep(2.0)
		waterSystem.servoSet(0)
		sleep(2.0)
		waterSystem.servoSet(160)
	quit()




if __name__ == '__main__':
    main()

