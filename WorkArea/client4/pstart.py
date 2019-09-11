import sys
from os import mkdir, chdir
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

	subRedList = ["thedickshow","investing"] #Our submissions go here.

	#save original output Path
	origOutPath = cO.outPath
	setattr(cO,"subCount",0)

	for sR in subRedList:
		listingGen = getattr(reddSess.subreddit(sR),"hot")
		submissionList = listingGen(limit=200)
		#Now archive the top 50 submissions
		cO.outPath += "/" + sR
		mkdir(cO.outPath)
		print(cO.outPath)
		for sub in submissionList:
			#setup our calls correctly.
			print("Num " + str(cO.subCount) + ", Currently Archiving submission:" + str(sub.id))
			currSubmission = pullredditsubmission(cO,reddSess,sub.id)
			ratemonitor(reddSess,cO)
			submissionoutput(cO,currSubmission,sub.id)
		cO.outPath = origOutPath

if __name__ == '__main__':
	defaultConfigName = "./config.txt"
	main(defaultConfigName)
