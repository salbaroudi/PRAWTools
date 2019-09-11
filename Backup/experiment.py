''' Version 0.1:
This script sets up a basic reddit session, so we can experiment with Object
structure and complex mining methods. Run with python3 ./experiment.py, and
use the main method to try out commands.

Notes on Objects used in main function below:
RedditSession Object -> Submission -> CommentForest -> MoreComments
 					 -> User -> Comments[New]
					 -> Subreddit -> Submission -> ...(see above)...

Submission Archive Purpose: Populate the CommentForest, and print it out in a
generated HTML. We replace the MoreComments objects in order
to get a full forest, of pure Comments.

Note: Comment Objects can be of NoneType if a user
(i) deletes their account
(ii) deletes their comment.

NOTE: It is assumed the comments are already ordered by timestamp; if praw
changes this requirement in the future, the recursive alg will have to sort
on its own!
'''
#Signature: List -> Object[Reddit Session]
#Purpose: Do OAUTH2 and gain access to remote Reddit API.
def startredditsession(credFilePath):
	credList = []
	credFP =  open(credFilePath, "r")
	for line in credFP:
		hold = line.split("::")
		credList.append(hold[1].replace('\n' , '')) #NewLine crashes auth code.
	r = praw.Reddit(client_id=credList[0],
	client_secret=credList[1], username=credList[2],  \
	password=credList[3], user_agent=credList[4])
	print(r.user.me()) #To see on CmdL that we did it properly.
	return r

def main():
    credFilePath = "/home/user/Documents/Universe/Credentials/reddit.txt"
    rS = startredditsession(credFilePath)

if __name__ == '__main__':
    main()
