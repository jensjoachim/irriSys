
import serial

class waterSerial:

	def __init__(self, port_s):
		self.port = serial.Serial(port_s, baudrate=9600, timeout=None)	
	
	def getPort(self):
		return self.port
	
	
