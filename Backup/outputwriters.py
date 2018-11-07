#This module contains all of our output writer functions, that get referenced by Our
#ConfigObject. We set them based on our output type (csv, html...etc).

#Signature: String -> Void
#Purpose: The final function that writes to output.
#Note: This does not append a new line. You have to do it!
def writeoutput(outFP,text):
	outFP.write(text)

#Signature: Object[Config] Object[Submission] -> NoneType
#Purpose: Given a filter function, apply to CommentForest and mutate nested objects.
def nofilter(cO,submission):
	pass #for now.

#Signature: Object[Config] Object[Submission] -> NoneType
#Purpose: Given a filter function, apply to CommentForest and mutate nested objects.
def afilter(cO,submission):
	pass #for now.

def htmlcommhead(delim, comm, outFP, depth):
	text = depth*delim
	text += "<div id=\'" + str(comm.id) + "\'"
	text += " class=\'" + "borders" + "\'>" + "\n"
	text += (depth + 1)*delim
	text += "<div><b>" + str(comm.author.name) + "</b></div>\n"
	writeoutput(outFP, text)

def htmlcommbody(delim, comm, outFP, depth):
	text = depth*delim + str(comm.body) + "\n"
	writeoutput(outFP, text)

def htmlcommfoot(delim,outFP, depth):
	writeoutput(outFP, (depth*delim + "</div>\n"))

#Purpose: The next few functions below pump out hardcoded HTML messages.
def htmlcommdelete(delim, outFP, depth):
	text = depth*delim
	text += "<div id=\'" + "deleted" + "\'>"
	text += " [DELETED] </div> \n"
	writeoutput(outFP,text)

#Signature: String Object[File Pointer] -> NoneType
#Purpose: Write header to output file.
def htmlsubheader(headerLoc,outFP):
	headFP = open(headerLoc,"r")
	for line in headFP:
		writeoutput(outFP,line)
	headFP.close()

#Signature: String Object[File Pointer] -> NoneType
#Purpose: Write footer. Redundant code refactor [***]
def htmlsubfooter(footerLoc,outFP):
	footFP = open(footerLoc,"r")
	for line in footFP:
		writeoutput(outFP,line)
	footFP.close()

#Signature: Submission[Object] -> void
#Purpose: This function pumps out selftext hardcoded HTML.
#You might want to not hardcode the index "-1" here; parameterize [***]
def htmlsubselftext(delim, sub,outFP):
	#[***]Optional Tab Depth for later
	text = "<h2>" + str(sub.title) + "</h2> \n"
	text += "<div id=\'selftext\' class=\'superborders\'>\n"
	text += 1*delim
	text += "<div><b>" + str(sub.author) + "</b></div>\n"
	text += delim + str(sub.selftext) + "\n"
	text += "</div>\n"
	text += "<br /><br />\n"
	writeoutput(outFP,text)

#Signature: X
#Purpose: Not Used. All work done in body for CSV methods.
def csvcommhead(delim, comm, outFP, depth):
	pass

#Signature:
#Purpose: Print out a comment that a user has made. Ignore the depth/structure.
def csvcommbody(delim, comm, outFP, depth):
	row = str(comm.id) + delim + str(comm.author.name) + delim
	row += str(comm.created) + delim + str(comm.body).replace("\n","").replace(delim,"") + "\n"
	outFP.write(row)

#Signature:
#Purpose: Not Used.
def csvcommfoot(delim,outFP, depth):
	pass

#Signature:
#Purpose: Print out a row that indicates a deletec comment is present.
def csvcommdelete(delim, outFP, depth):
	row = "DELETED" + delim + "NoAuthor" + delim
	row += str(-1) + delim + "DELETED" + delim + "\n"
	outFP.write(row)

#Signature:
#Purpose: print a simple header.
def csvsubheader(headerLoc,outFP):
	row = "ID,User,DateCreated,Text\n"
	outFP.write(row)

#Signature:
#Purpose: Not Used.
def csvsubfooter(footerLoc,outFP):
	pass

#Signature:
#Purpose: Format: Comment Number, Submission ID, user, date, title
# Comment Number, Submission ID, user, date, selftext (formatted)
def csvsubselftext(delim,sub,outFP):
	row = str(sub.id) + delim + str(sub.author) + delim
	row += str(sub.created) + delim + str(sub.title) + "\n"
	outFP.write(row)
	row = str(sub.id) + delim + str(sub.author) + delim
	row += str(sub.created) + delim + str(sub.selftext).replace(delim,"").replace("\n","") + "\n\n"
	outFP.write(row)
