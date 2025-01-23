To run the code, simply type "python3 Parser.py" in your chosen command line interface, it will prompt you for a file you want to read in. The following files can be read in:


	These are input files that will produce no errors:
		- dictTest.txt
		- listTest.txt
		- listInPair.txt
		- ListInDictInList.txt
		- dictInListThenList.txt
		- dictInList.txt
		
	NOTE THAT INPUT FILES ARE CASE SENSITIVE
		
	These are input files that will showcase error handling:
		- missingBrace.txt
		- missingComma.txt
		- missingBracket.txt
		- numberforkey.txt
		
	All files listed have a corresponding output file already. they are all the same file name, with output as a suffix.
		ex: missingBrace.txt has output file called missingBraceoutput.txt
		These will not run if inputted into the program, they purely show the output
		of each file.
	
	to view the output, open parseroutput.txt
	
Assumptions:

	- The input files were created using my own scanner, using someone
	else's scanner to generate input files will not work.
	- The parse tree is represented using indentation, where non-terminals (e.g., list, dict) increase
	the indentation level, and terminals appear under their respective parent nodes.
	- The program assumes the user will input a text file. Input a provided text file to see the program running
	- The parser distinguishes between STRING values (used in lists or values) and PAIRSTRING keys (used in dictionaries).
	This is just a solution I had for an issue I was encountering. Both will still output the exact same, they are just
	handled differently in the back end.
	- parseroutput.txt is where you will find the output of whatever file you read in last.
	What is there currently is just what I ran in the program last before pushing.
	- ignore the .idea folder, this is just there because I used IntelliJ as my IDE of choice.