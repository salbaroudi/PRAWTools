import getopt
import sys
import os
from pbase import *

#Globals: Note: These are guarenteed to only be used in one place.
#So no development/RT errors should result from this global usage.
helpString = '''Usage of PRAW Archiver:

parch -hv -s [url] -S [Input file]
	- h: help string
	- v: version and creator info.
	- s: archive a submission
	- S: archive a list of submissions; give the *path* to this file.
'''
versionString = '''
PRAW Archiver v0.4. Created by Sean al-Baroudi (sean.al.baroudi@gmail.com).
'''

#Signature: Dict -> Dict
#Purpose: For script configuration, lets read from an external config file
def readconfig(cO,configLoc):
	fpConfig = open(configLoc, "r")
	for line in fpConfig:
		hold = line.split("::")
		hold[1] = hold[1].replace("\n","")
		if (hold[1].isdigit()):
			setattr(cO,hold[0],int(hold[1]))
		elif (hold[1] != ""):
			setattr(cO,hold[0],hold[1])
		else:
			pass #do not add attribute
	fpConfig.close()

#Signature: Dict -> Dict
#Purpose: Process the command line arguments, and set up states
#to guide our program.
def processargs(cO):
	try:
		opts, args = getopt.getopt(sys.argv[1:], "hvs:S:o:")
		if (len(opts) == 0):
			print("ERROR: No options provided. Aborting.")
			sys.exit(2)
	except getopt.GetoptError as err:
		print(err)
		sys.exit(2)
	for o, a in opts:
		if o == "-h":
			print(helpString)
			sys.exit(2)
			break
		elif o == "-v":
			print(versionString)
			sys.exit(2)
			break
		elif (o == "-s" and  a != ""):
			setattr(cO,'threadURL',a)
			print("ThreadURL:" + cO.threadURL)
		elif (o == "-S" and  a != ""):
			setattr(cO,'inPath',a)
			print("inPath:" + cO.inPath)
		elif (o == "-o" and a != ""):
			setattr(cO,'outPath',a)
			print("outPath:" + cO.outPath)
		else:
			print("ERROR: An unrecognized option or format has appeared.")
			print("Please check your argument string.")
			sys.exit(2)

	#Check if minimum settings found: an output folder, and path/threadURL:
	if (not (hasattr(cO,"outPath") and (hasattr(cO,"inPath") or hasattr(cO,"threadURL")))):
		print("ERROR: Either -o not specified correctly, or -s/S not specified correctly. Check formatting." )
		sys.exit(2)

#Signature: Object[ConfigObject] -> NoneType
#Purpose: apply checks to params, to ensure settings don't clobber.
#Also, set properties such as delimiter, writers, etc.
def setparams(cO):
	#Set Delimiter
	cO.delimSymbol = (cO.delimSymbol).lower()
	if (cO.delimSymbol == "tab"):
		cO.delimSymbol = "\t"
	elif (cO.delimSymbol == "comma"):
		cO.delimSymbol = ","
	elif (cO.delimSymbol == "colon"):
		cO.delimSymbol = ":"
	elif (cO.delimSymbol == "semicolon"):
		cO.delimSymbol = ";"
	elif (cO.delimSymbol == "tilde"):
		cO.delimSymbol = "~"
	elif (cO.delimSymbol == ""):
		pass
	else:
		print("Error:: Invalid delimiter symbol specified in config file.")
		sys.exit(2)

	#Toggle Read Only Mode
	if (cO.readOnly == 1):
		cO.readOnly = True
	elif (cO.readOnly == 0):
		cO.readOnly == False
	else:
		print("Error:: Invalid readOnly setting specified in config file.")
		sys.exit(2)

	#Convert the Replace More Limits and Settings to integers.
	if(cO.rmLimit != "None"):
		cO.rmLimit = int(cO.rmLimit)
	else:
		cO.rmLimit = None #None is an internal type!!
	cO.rmThresh = int(cO.rmThresh)

	#Convert sleep time:
	cO.sleepTime = int(cO.sleepTime)

	#Set output writers
	if (cO.outputType == "html"):
		cO.setsubwriters(htmlsubheader,htmlsubselftext,htmlsubfooter)
		cO.setcommwriters(htmlcommhead,htmlcommbody,htmlcommfoot,htmlcommdelete)
	elif (cO.outputType == "json"):
		print("JSON output is currently not implemented. Aborting.")
		sys.exit(2)
	elif (cO.outputType == "csv"):
		cO.setsubwriters(csvsubheader,csvsubselftext,csvsubfooter)
		cO.setcommwriters(csvcommhead,csvcommbody,csvcommfoot,csvcommdelete)
	else:
		print("Error:: Invalid output format specified in config file.")
		sys.exit(2)

	#Set commment tree filter:
	if (cO.cFFilter == "None"):
		cO.setfilter(nofilter)
	else:
		cO.setfilter(afilter)

	#For our outPath setting, lets make a folder if it doesn't exist.
	if (not os.path.exists(cO.outPath)):
		os.mkdir(cO.outPath)
	else:
		print("WARNING: " + cO.outPath + "already exists; old results might be clobbered.")

#Signature: List -> Object[Reddit Session]
#Purpose: Do OAUTH2 and gain access to remote Reddit API.
def startredditsession(cO):
	credList = []
	credFP =  open(cO.credFile, "r")
	for line in credFP:
		hold = line.split("::")
		credList.append(hold[1].replace('\n' , '')) #NewLine crashes auth code.
	r = ""
	if (cO.readOnly):
		r = praw.Reddit(client_id=credList[0],
		client_secret=credList[1],user_agent=credList[4])
	else:
		r = praw.Reddit(client_id=credList[0],
		client_secret=credList[1], username=credList[2],  \
		password=credList[3], user_agent=credList[4])
		print(r.user.me()) #wont work in read only mode!

	credFP.close()
	return r

#Signature: Void -> Void.
#Purpose: Our main method that acts as the scope for all functions.
#Implemented this way to avoid heavy usage of global variables.
def main(dCN):
	cO = ConfigObject()
	processargs(cO)
	readconfig(cO, (cO.outPath + "/" + dCN))
	setparams(cO)
	reddSess = startredditsession(cO)

	subList = [] #Our submissions go here.
	if ("threadURL" in vars(cO)): #vars just outputs obj.__dict__ special attribute.
		subList.append(url2id(cO.threadURL))
	elif ("inPath" in vars(cO)):
		subList = urlFile(cO.inPath)

	for subID in subList:
		popsubmission = pullredditsubmission(cO,reddSess,subID)
		ratemonitor(reddSess,cO)
		cO.cffilter(cO,popsubmission)
		submissionoutput(cO,popsubmission,subID)

if __name__ == '__main__':
	defaultConfigName = "config.txt"
	main(defaultConfigName)
