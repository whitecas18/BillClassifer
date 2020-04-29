This is a readme.txt on how to use our summarizer/classifier program.

**STARTING PROGRAM:

-To run program correctly, the program must be initialized by running UserInterface.py. The program can not be run by starting any other module.


**NECESSARY LIBRARIES/IMPORTS:

-Gensim
-numpy
-asciiplotlib
-matplotlib
-json
-requests
-datetime
-math
-os


**NOTES ABOUT RUNNING PROGRAM:

-For *package bills*, the government api sorts these by *upload date* and not issue date.
if you are searching for a bill from a certain date, this will not find it, you must use general bills.
General bills can be searched by bill issue/creation date.

-Some very large bills summaries take a few minutes to load, if it seems like the program hangs up, it is probably loading a summary so be patient.

-Some summaries have repeated sentences, this is a known issue, and is due to quirks in the .gov api.

-All folder's(train and test folder) must remain in their location. They must be in the working directory for the program to work as intended.