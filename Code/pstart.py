import sys
print(str(sys.path))
sys.path.append("/home/user/Documents/Workspace/CodeProjects/PRAW/PRAW_Tools/ParchCodeBase")
print(str(sys.path))
from parch import *


#starting template!
#Signature: Void -> Void.
#Purpose: Our main method that acts as the scope for all functions.
#Implemented this way to avoid heavy usage of global variables.
def main(dCN):
	cO = ConfigObject()
	processargs(cO)
	readconfig(cO, dCN)
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
	defaultConfigName = "./config.txt"
	main(defaultConfigName)
