

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



	# Set device
	device_name = "nano328"
	#device_name = ""
	
	# Set Serial port
	serial_port = "/dev/ttyUSB0"
	#serial_port = "/dev/ttyACM0"
	
	#build(device_name)
	#upload(device_name,serial_port)
	
	#runCommand("./ino_cmds.sh -b -m nano328 -p /dev/ttyUSB0")
	os.system("./ino_cmds.sh -b -u -m nano328 -p /dev/ttyUSB0")
	#quit()

	waterSystem = water(serial_port)
	runCommand("rm log")	# Clear log
	waterSystem.waterIn(300)
	quit()
	
	while 1:
		print waterSystem.scaleReadCont(2)
		
	while 1:
		sleep(2.0)
		waterSystem.servoSet(100)
		sleep(2.0)
		waterSystem.servoSet(120)
	quit()




if __name__ == '__main__':
    main()

