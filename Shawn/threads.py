import threading



#Creates a thread for the function you want to run.
#fuctionToRun: pass as just the name of the function (not in quotes)
#argsToPass: pass the arguments of the function to run in a list 
def runFunction(functionToRun, argsToPass):
	if argsToPass:
		x = threading.Thread(target=functionToRun, args = argsToPass)
	else:
		x = threading.Thread(target=functionToRun)

	x.start()



#Example below
'''
def printme(x, y):
	print(x)
	print(y)

runFunction(printme, ["hi there", "My name is Bot"])
'''