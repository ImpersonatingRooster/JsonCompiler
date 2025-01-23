Final project part 1

I have chosen to write a scanner that scans key-value pairs, arrays, and objects.
There are 12 tokens in total:

	- Left Braces: {
	- Right Braces: }
	- Left Brackets: [
	- Right Brackets: ]
	- Colon: :
	- Comma: ,
	- Strings: "key", "value"
	- Integers: e.g., 123
	- Floating-point numbers: e.g., 45.67
	- Booleans: true, false
	- Null: null
	- EOF
	
	
How to use:
	have a .txt file you wish to tokenize in the same directory as scanner.py
	run scanner.py
	console will prompt you to enter the file name. include the extension. .json or .txt will work.
	
Assumptions:
	The input files are well-formed JSON files.
	The lexer is designed to handle JSON-specific tokens such as the ones specified above.
	Whitespace gets ignored and isn't tokenized.
	the t and f in true or false is always lowercase.
	
Key parts of code:
	Lexer class: This is the meat of the program. It handles the tokenization process, the get_next_token() method is what moves through the input and detects the token. tokenize() collects all the tokens and then sends that back to the main method
	LexerError class: This class gets called when there is some sort of error with the input file
	Token class: this is what formats and sends the token to the output. get_next_token() calls this class once it finds the right token type, and sends what is returned to tokenize().
		
	