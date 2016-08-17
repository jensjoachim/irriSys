import os
import subprocess

from waterSerial import *
from waterMod import *

from time 		import gmtime, strftime 

import os.path

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

	PUMP_CHILI_TOP = 0
	PUMP_CHILI_BOT = 1
	
	
	
	# # Get the time for new measurement
	# ss = waterLog.getTime()
	
	
	# # Check if file is there
	# fileNameWaterIn = "in_%i.txt" % (PUMP_CHILI_BOT)
	# if os.path.isfile(fileNameWaterIn):
		# # Then read last value
		# with open(fileNameWaterIn) as fileWaterIn:
			# lines = fileWaterIn.readlines()
			# lastLine = lines[-1]
			# lastLineSec = lastLine.split(' ',4)
			# nextAmount = int(lastLineSec[4])
			# #print nextAmount
	# else:
		# # If not then make the file
		# with open(fileNameWaterIn, "a") as fileWaterIn:
			# fileWaterIn.write("")
			# nextAmount = 10

			
	# # Connect to serial
	# waterSystem = water(serial_port)	
	
	
	# # Water PUMP_CHILI_TOP
	# waterSystem.waterIn(nextAmount)
	# waterSystem.waterTo(PUMP_CHILI_BOT,nextAmount/5+20)
	# sleep(5.0) # !!!!!!
	# # sleep(60.0*2)
	# sum = 0
	# sum = waterSystem.waterOut()
	
	# # Log waterOut
	# fileNameWaterOut = "out_%i.txt" % (PUMP_CHILI_BOT)
	# with open(fileNameWaterOut, "a") as nextAmountFile:
		# amountText = ""+ss+" Amount: %i\n" % (sum)
		# nextAmountFile.write(amountText)
		
	# # Update WaterIn
	# if sum < 10:
		# nextAmount = int(float(nextAmount) * (1.0 + 0.2));
	# else:
		# nextAmount = nextAmount + (int(float(nextAmount) * 0.2) - sum)
		
	# with open(fileNameWaterIn, "a") as fileWaterIn:
		# textWaterIn = ss+" %i \n" % (nextAmount)
		# fileWaterIn.write(textWaterIn)
		
		
	# Connect to serial
	waterSystem = water(serial_port)	
	waterSystem.autoWater(PUMP_CHILI_BOT,10)	
	
	
	
	# Water PUMP_CHILI_TOP
	#waterSystem.waterIn(AMOUNT_CHILI_TOP)
	#waterSystem.waterTo(PUMP_CHILI_TOP,PUMP_TIME_CHILI_TOP)
	#sleep(20.0)
	#waterSystem.waterOut()

	sleep(20.0)
		
	quit()
	
if __name__ == '__main__':
    main()

