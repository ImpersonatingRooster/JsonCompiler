#This structure follows the scanner example we were given in tutorial. I have adjusted it to have the scanner recognize .json files.

class TokenType:
    LBRACE = 'LBRACE' #'{'
    RBRACE = 'RBRACE' #'}'
    LBRACK = 'LBRACK' #'['
    RBRACK = 'RBRACK' #']'
    COL = 'COL' #':'
    COM = 'COM' #','
    STR = 'STR' #string
    INT = 'INT' #integer
    FLOAT = 'FLOAT' #floating point integer
    BOOL = 'BOOL' #'true|false'
    NULL = 'NULL' #'null'
    EOF = 'EOF' #end of file
     
class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        if self.type == TokenType.STR:
            return f"<str, {self.value}>"
        elif self.type == TokenType.LBRACE:
            return f"<lbrace, {self.value}>"
        elif self.type == TokenType.RBRACE:
            return f"<rbrace, {self.value}>"
        elif self.type == TokenType.LBRACK:
            return f"<lbrack, {self.value}>"
        elif self.type == TokenType.RBRACK:
            return f"<rbrack, {self.value}>"
        elif self.type == TokenType.COL:
            return f"<col, {self.value}>"
        elif self.type == TokenType.COM:
            return f"<com, {self.value}>"
        elif self.type == TokenType.INT:
            return f"<int, {self.value}>"
        elif self.type == TokenType.FLOAT:
            return f"<float, {self.value}>"
        elif self.type == TokenType.BOOL:
            return f"<bool, {self.value}>"
        elif self.type == TokenType.NULL:
            return f"<null, {self.value}>"
        elif self.type == TokenType.EOF:
            return f"<eof, {self.value}>"
        
class LexerError(Exception):
    def __init__(self, position, character):
        self.position = position
        self.character = character
        super().__init__(f"Invalid character '{character}' at position {position}")
    
class Lexer:
    def __init__(self, input_text):
        self.input_text = input_text
        self.position = 0
        self.currentChar = self.input_text[self.position] if self.input_text else None

    def advance(self):
        self.position += 1
        if self.position >= len(self.input_text):
            self.currentChar = None
        else:
            self.currentChar = self.input_text[self.position]

    def ignore_whitespace(self):
        while self.currentChar is not None and self.currentChar.isspace():
            self.advance()
    
    #this method is purely used for numOrFloat()
    def isValidChar(self):
        characterCheck = self.currentChar
        # check if the current character is one of the valid characters
        if characterCheck in ['{', '}', '[', ']', ':', ',', 'n', 't', 'f', '"']:
            return True
        
        # return False if none of the conditions are met
        return False
        
        
    def get_next_token(self):
        while self.currentChar is not None:
            if self.currentChar.isspace():
                self.ignore_whitespace()
                continue
            if self.currentChar == "{":
                self.advance()
                return Token(TokenType.LBRACE, '{')
            if self.currentChar == "}":
                self.advance()
                return Token(TokenType.RBRACE, '}')
            if self.currentChar == "[":
                self.advance()
                return Token(TokenType.LBRACK, '[')
            if self.currentChar == "]":
                self.advance()
                return Token(TokenType.RBRACK, "]")
            if self.currentChar == ":":
                self.advance()
                return Token(TokenType.COL, ':')
            if self.currentChar == ",":
                self.advance()
                return Token(TokenType.COM, ',')
            if self.currentChar.isdigit():
                return self.numOrFloat()
            if self.currentChar == '"':
                return self.recognize_string()
            if self.currentChar == "t":
                return self.recognize_bool()
            if self.currentChar == "f":
                return self.recognize_bool()
            if self.currentChar == "n":
                return self.recognize_null()
            else:
                raise LexerError(self.position, self.currentChar)
        return Token(TokenType.EOF)

    def tokenize(self):
        tokens = []
        while True:
            try:
                token = self.get_next_token()
            except LexerError as e:
                print(f"Lexical error: {e}")
                break
            if token.type == TokenType.EOF:
                break
            tokens.append(token)
        return tokens

    def recognize_null(self):
        result = ''
        expected = 'null'

        for char in expected:
            if self.currentChar is not None and self.currentChar == char:
                result += self.currentChar
                self.advance()
            else:
                raise LexerError(self.position, f"{self.currentChar} when trying to recognize null")
        return Token(TokenType.NULL, result)

    def recognize_bool(self):
        result = ''
        expected = ''
        if self.currentChar == "t":
            expected = 'true'
        elif self.currentChar == 'f':
            expected = 'false'
        for char in expected:
            if self.currentChar == char and not None:
                result += self.currentChar
                self.advance()
            else:
                raise LexerError(self.position, f"{self.currentChar} when trying to recognize true or false")
        
        return Token(TokenType.BOOL, result)
            

    def numOrFloat(self):
        result = ''
        isFloat = False
        isError = False
        periodCount = 0
        while self.currentChar is not None and not self.currentChar.isspace() and self.isValidChar() is False:
            if (self.currentChar == "." and periodCount < 1):
                isFloat = True
                periodCount += 1
                result += self.currentChar
                self.advance()
            elif (self.currentChar == "." and periodCount > 0):
                isError = True
                result += self.currentChar
                self.advance()
            elif (self.currentChar.isdigit()):
                result += self.currentChar
                self.advance()
            else:
                break
            
        if isError:
            raise LexerError(self.position, f"Invalid character in number {result}")
        if isFloat:
            return Token(TokenType.FLOAT, result)
        else:
            return Token(TokenType.INT, result)


    def recognize_string(self):
        result = '"'
        #first " was recognized outside of this method, so move one char forward
        self.advance()

        #continue until you see closing "
        while self.currentChar != '"' and self.currentChar != None:
            result += self.currentChar
            self.advance()

        if self.currentChar == '"':
            result += self.currentChar
            self.advance()
            return Token(TokenType.STR, result)
        else:
            raise LexerError(self.position, "Unterminated string")
        
            
#w3 schools helped me learn how to read and write from a file.
if __name__ == "__main__":
    input_file = open(input('Type in the file name you would like to read in from\n'), "r").read()
    lexer = Lexer(input_file)
    tokens = lexer.tokenize()

    with open("output.txt", "w") as out:
        for token in tokens:
            print(token)
            out.write(str(token) + "\n")
