import praw
from pprint import pprint
from time import sleep
from outputwriters import *
import re

'''
This class contains all of our configuration information. It is passed through
the call stack, keeping track of everything.

"cO" stands for Configuration Object
'''
class ConfigObject(object):
	''' This is an empty class, in which dynamic attributes are added from the
	Configuration File that parch uses. This way, we can attach output functions
	to attributes, without them being BOUND at the interpretation state of python.
	'''
	#Signature: NoneType -> NoneType
	#Purpose: Empty Constructor
	def __init__(self):
		pass

	#Signature: Fun Fun Fun Fun -> NoneType
	#Purpose: Use an instance method to set subreddit writers.
	#These are unbound functions.
	def setsubwriters(self,head,self_,foot):
		setattr(self, "subHead", head)
		setattr(self, "subSelf", self_)
		setattr(self, "subFoot", foot)

	#Signature: Fun Fun Fun Fun -> NoneType
	#Purpose: Use an instance method to set our comment writers!
	#These are unbound functions.
	def setcommwriters(self,head,body,foot,del_):
		setattr(self, "commHead", head)
		setattr(self, "commBody", body)
		setattr(self, "commFoot", foot)
		setattr(self, "commDel", del_)

	#Signature: Fun -> NoneType
	#Purpose: Set comment tree filter
	def setfilter(self, filt):
		setattr(self,"cffilter",filt)


#Signature: String -> String
#Purpose: Extract thread Hex ID from URL string.
def url2id(url):
	urlRe = re.compile("(/comments/([a-zA-Z0-9_]{6,6})/)") #ID is exactly 6 characters
	return (urlRe.search(url)).group(2)

#Signature: String[Path] -> Dict[String]
#Open the URL file, read each URL line by line and separate Base36 IDs
def urlFile(inPath):
	fpIn = open(inPath, "r")
	newList = []
	for url in fpIn:
		newList.append(url2id(url)) #just grab the base36 hex id
	fpIn.close()
	return newList

#Signature: String -> List[String]
#Purpose: Open up a path and get a list of subreddits (in the file).
def readsrfile(inPath):
	fpIn = open(inPath, "r")
	newList = []
	for name in fpIn:
		newList.append(name) #just grab the base36 hex id
	fpIn.close()
	return newList

#Signature: Object[RedditSession] Object[Config] -> NoneType
#Purpose: This will only be invoked if we have a very heavy load. It is to avoid
#being booted out by the reddit servers if we pull too much data (be nice).
#Technically, since version ~4 or 5 of PRAW, the framework automanages this.
#However, on the multi-instance page:
#http://praw.readthedocs.io/en/latest/getting_started/multiple_instances.html
#it is mentioned that in extreme cases (lots of hungry threads),
#the automanagement may not work propertly.
#This is just for safety.
def ratemonitor(reddSess,cO):
	if (cO.readOnly == 0):
		if (reddSess.auth.limits['remaining'] < 25.0):
			print("Warning: remaining API calls under 25; sleeping for " + str(cO.sleepTime) + " seconds.")
			sleep(cO.sleepTime)
	else:
		if (cO.subCount > 9):
			print("Warning: We have pulled 10 submissions in Read Only mode. Sleeping for a 15s...")
			sleep(15)
			cO.subCount = 0
			print("Sleep has ended. Continuing job...")
		else:
			cO.subCount += 1


#Signature: Comment[Obj] Int -> Void
#Purpose: We recursively go through the
#comment replies, and encase them in HTML.
def commrec(cO, comm, outFP, depth):
	if ((comm.body is None) or (comm.author is None)):
		cO.commDel(cO.delimSymbol,outFP, depth)
	else:
		cO.commHead(cO.delimSymbol,comm, outFP, depth)
		cO.commBody(cO.delimSymbol,comm,outFP,depth)
	if (comm.replies is not None): #a node [***] Could we not mix looping and recursion?
		for reply in comm.replies:
			commrec(cO, reply, outFP, (depth + 1))
	cO.commFoot(cO.delimSymbol, outFP, depth) #leaf and node have same ending.
	return

#Signature: Comment[Obj] -> Void
#Purpose: Wrapper for our comment printing.
def commentrecurse(cO,comm,outFP):
	commrec(cO,comm,outFP,0)

def submissionoutput(cO,submission,subID):
	if (cO.outputType == "html" or cO.outputType == "json"):
		submissionoutputtree(cO,submission,subID)
	elif (cO.outputType == "csv"):
		submissionoutputflat(cO,submission,subID)

def submissionoutputtree(cO,submission,subID):
	#Lets form our HTML document.
	outFP = open(cO.outPath + "/" + subID + "." + cO.outputType, "w") #will create one automatically.
	cO.subHead(cO.headLoc,outFP)
	cO.subSelf(cO.delimSymbol,submission,outFP)
	#Lets parse the CommentForest, and print it nicely.
	for comment in (submission.comments): # .list() top level comments only? Or flattens all of them? [***]
		commentrecurse(cO,comment,outFP)
	cO.subFoot(cO.footLoc,outFP)
	outFP.close()

def flatcomment(cO,comm,outFP,depth):
	if ((comm.body is None) or (comm.author is None)):
		cO.commDel(cO.delimSymbol, outFP, depth)
	else:
		cO.commHead(cO.delimSymbol,comm, outFP, depth)
		cO.commBody(cO.delimSymbol,comm,outFP,depth)
	#There is no recursion for flat comments.
	cO.commFoot(cO.delimSymbol, outFP, depth) #leaf and node have same ending.

def submissionoutputflat(cO,submission,subID):
	#Lets form our HTML document.
	outFP = open(cO.outPath + "/" + subID + "." + cO.outputType, "w") #will create one automatically.
	cO.subHead(cO.headLoc,outFP)
	cO.subSelf(cO.delimSymbol,submission,outFP)
	#Lets parse the CommentForest, and print it nicely.
	for comment in (submission.comments).list(): # .list() top level comments only? Or flattens all of them? [***]
		flatcomment(cO,comment,outFP,0)
	cO.subFoot(cO.footLoc,outFP)
	outFP.close()

#Signature: Object[ConfigObject] Object[Reddit Session] String[id] -> Object [Comment Forest]
#Purpose: We create an HTML wrapper page, with nested comments that
#mirrors the submission page and all its comments.
def pullredditsubmission(cO,reddSess,subID):
	submission = reddSess.submission(id=subID)
	submission.comments.replace_more(limit=cO.rmLimit, threshold=cO.rmThresh) #get everything!
	return submission
