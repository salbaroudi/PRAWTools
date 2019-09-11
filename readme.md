### Purpose: PArch - PRAW wrapper library, for Archiving Reddit Posts and Submissions.

This wrapper library automates and simplifies large data pulls, for the PRAW library in python.
It is designed to pull large numbers of comments and submissions from subreddits, with high-level
functional calls.


###Running the Code:

- The code has been modularized and template files for conceptual ease.

- I also want a workspace where I can do client work, or develop new branches
of the parch code.

In order to achieve these two goals, I changed the folder structure, as follows:

PRAW
  ./PRAW_Tools
  |---/ParchCodeBase: All the code base files live here
  |---/Templates
       |---input.txt
       |---codetemplates
       |---config.txt
       |---various headers/footers for outputwriters
  |---/WorkArea
      |---/Various Projects
 - newproj.sh

Because project work, CodeBase, Templates are all nested
at different levels, it can be difficult to setup a new working folder. At the top
level of the PRAW_Tools folder, a shell script (newproj.sh) has been written to
set up the correct folder structure:

/WorkArea
   /<PROJECTNAME>
      /<OUTPUTFOLDER>
      -- input.txt
      -- config.txt
      -- pstart.py

The shellscript takes the following options on command line, and is run as follows:

./newproj.sh <PROJECTNAME> <OUTPUTFOLDER>

After this is done, remember to populate the input.txt file (if used).
Also, look at the config.txt carefully, to make sure the right options have been
chosen.


###Running PArch

Once the configuration script has been run, see the .odt file for a list of parameters on 
how to run PRAW.

**END**
