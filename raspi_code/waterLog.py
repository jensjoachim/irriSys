
from time 		import gmtime, strftime 
import inspect

def log(s0, s1):
	# s0 = "E" 			<- Log error and EXIT
	# s0 = "I"			<- Log and print message
	# s0 = ""			<- Log method
	# s1 = "Hej hej"	<- Message
	if s0 == "E":
		output = "ERROR: " + strftime("%d %b %Y %H:%M:%S", gmtime()) + " " + inspect.stack()[1][3] + "() " + s1 + "\n"
		file = open("log", "a")
		file.write(output)
		print output # Print message in terminal
		i = 1
		s = ""
		# trace back
		while inspect.stack()[i][3] != "main":
			s = s + "\n" + inspect.stack()[i][3] + "() "
			i = i + 1
			
		s = s + "\n" + inspect.stack()[i][3] + "() "	
		print s
		file = open("log", "a")
		file.write(s)
		quit()	# And quit
	elif s0 == "I":	
		msg = strftime("%d %b %Y %H:%M:%S", gmtime()) + " INFO: "+ s1 + "\n"
		file = open("log", "a")
		file.write(msg)
		print s1
	else:
		output = strftime("%d %b %Y %H:%M:%S", gmtime()) + " " + inspect.stack()[1][3] + "() " + s1 + "\n"
		file = open("log", "a")
		file.write(output)

def getTime():
	return "" + strftime("%d %b %Y %H:%M:%S", gmtime())