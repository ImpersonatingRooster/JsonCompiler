To run the code, simply type "python3 Parser.py" in your chosen command line interface, it will prompt you for a file you want to read in. The following files can be read in:


	These are input files that will produce no errors:
		- dictTest.txt
		- listTest.txt
		- listInPair.txt
		
	NOTE THAT INPUT FILES ARE CASE SENSITIVE
	
		These are input files that will showcase error handling:
		- type1test.txt
		- type2test.txt
		- type3test.txt
		- type4test.txt
		- type5test.txt
		- type6test.txt
		- type7test.txt
	
	to view the output, open parseroutput.txt
	
	All error files listed have a corresponding file that shows the file in its original, untokenized json form.
	All files are named just like the corresponding error file name, with "JSONform" as a suffix.
	type1test.txt has a file name type1testJSONform.txt, etc.
	DO NOT ATTEMPT TO RUN THESE FILES IN THE PROGRAM, IT WILL NOT WORK
	
Assumptions:

	- The input files are all syntactically correct.
	- The program assumes the user will input a text file
	- parseroutput.txt is where you will find the output of whatever file you read in last.
	What is there currently is just what I ran in the program last before pushing.
	- ignore the .idea folder, this is just there because I used IntelliJ as my IDE of choice.