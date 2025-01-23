

class GrammarType:
    VALUE = 'VALUE' #dict|list|STRING|NUMBER|"true"|"false"|"null"
    LIST = 'LIST' #'[' value (',' value)* ']'
    STRING = "STRING:"
    PAIRSTRING = "pSTRING"
    NUMBER = "NUMBER:"
    NULL = "NULL"
    PAIR = "PAIR"
    DICT = "DICT"
    BOOL = "BOOL"
    LBRACE = 'LBRACE' #'{'
    RBRACE = 'RBRACE' #'}'
    LBRACK = 'LBRACK' #'['
    RBRACK = 'RBRACK' #']'
    COL = 'COL' #':'
    COM = 'COM' #','
    UNKNOWN = "UNKNOWN"
    # EOF = 'EOF' #end of file


class Grammar:
    def __init__(self, label=None, value=None, is_terminal=None):
        self.label = label
        self.value = value
        self.is_terminal = is_terminal
    
    def __repr__(self):
            if self.label == GrammarType.VALUE:
                return "value"
            elif self.label == GrammarType.LIST:
                return "list"
            elif self.label == GrammarType.STRING:
                return f"{self.value}"
            elif self.label == GrammarType.NUMBER:
                return f"{self.value}"
            elif self.label == GrammarType.NULL:
                return "NULL"
            elif self.label == GrammarType.PAIR:
                return f"{self.value}"
            elif self.label == GrammarType.DICT:
                return f"{self.value}"
            elif self.label == GrammarType.BOOL:
                return f"{self.value}"
            elif self.label == GrammarType.LBRACE:
                return f"{self.value}"
            elif self.label == GrammarType.RBRACE:
                return f"{self.value}"
            elif self.label == GrammarType.LBRACK:
                return f"{self.value}"
            elif self.label == GrammarType.RBRACK:
                return f"{self.value}"
            elif self.label == GrammarType.COL:
                return f"{self.value}"
            elif self.label == GrammarType.COM:
                return f"{self.value}"
            elif self.label == GrammarType.PAIRSTRING:
                return f"{self.value}"
            else:
                return ""

class Parser:
    def __init__(self, input_text):
        self.position = 0
        self.lookAhead = 0
        self.eatError = []
        self.hasError = False
        self.errorLocation = []
        #import the file into a string variable
        self.input_text = input_text

        #split each token into an array
        self.token_list = []

        #found how to split by line on w3schools
        self.token_list = input_text.splitlines()

        #start at first token
        self.current_token = self.token_list[self.position]
        
    
    
    def advance(self):
        self.position += 1
        if (self.position < len(self.token_list)):
            self.current_token = self.token_list[self.position]

        #if its a blank line, advance
        while self.position < len(self.token_list) and self.current_token.isspace():
            self.advance()

    def eat(self, token_type):
        errorMessage = ""

        token = self.current_token.split()
        if token_type in token[1]:
            self.advance()
        else:
            errorMessage = f"Expected token '{token_type}' got '{token[1].strip('>')}'  at line {self.position + 1} in input file"
            print(f"Expected token '{token_type}' got '{token[1].strip('>')}' at line {self.position + 1} in input file")
            self.eatError.append(errorMessage)
            self.errorLocation.append(self.position)
            self.hasError = True
            self.advance()
        
    def parse(self):
        parseList = [self.determineType()]
        outputList = self.output(parseList)
        if self.hasError:
            for i in range(len(self.eatError)):
                outputList.append(self.eatError[i])
        return outputList
    def semanticCheck(self, list):
        keyList = []
        listType = []
        def type1check(item):
            word = item.value
            if word[0] == "." or word[-1] == ".":
                semanticMessage = f"Type 1 Error at '{item}': Invalid Decimal Number"
            else:
                semanticMessage = "clear"
            return semanticMessage

        def type2check(item):
            word = item.value
            if word == "":
                semanticMessage = f"Type 2 Error at '{item}': Empty key"
            else:
                semanticMessage = "clear"
            return semanticMessage
        def type3check(item):
            word = item.value
            if len(word) > 1:
                if word[0] == "0":
                    if word[1] == ".":
                        semanticMessage = "clear"
                    else:
                        semanticMessage = f"Type 3 Error at '{item}': Improper formatting"
                elif word[0] == "+":
                    semanticMessage = f"Type 3 Error at '{item}': Improper formatting"
                else:
                    semanticMessage = "clear"
            else:
                if word[0] == "+":
                    semanticMessage = f"Type 3 Error at '{item}': Improper formatting"
                else:
                    semanticMessage = "clear"
            return semanticMessage
        def type4check(item):
            word = item.value
            if word == "true" or word == "false":
                semanticMessage = f"Type 4 Error at '{item}': Reserved word"
            else:
                semanticMessage = "clear"
            return semanticMessage
        def type5check(item):
            word = item.value
            if word in keyList:
                semanticMessage = f"Type 5 Error at '{item}': Non-unique key"
            else:
                semanticMessage = "clear"
                keyList.append(word)
            return semanticMessage
        def type6check(item):
            #was having issues with modifying the global listType variable, found nonlocal function
            #on w3schools https://www.w3schools.com/python/ref_keyword_nonlocal.asp
            nonlocal listType
            changeNext = False
            #The case that this is the first list
            if len(listType) == 0:
                listType.append(item.label)
                semanticMessage = "clear"
            #the case where the list element type does not equal list type
            elif item.label == GrammarType.COM or item.label == GrammarType.RBRACK:
                semanticMessage = "clear"
            elif item.label != listType[-1]:
                semanticMessage = f"Type 6 Error at '{item}': Inconsistent list element datatype"
            else:
                semanticMessage = "clear"
            return semanticMessage
        def type7check(item):
            word = item.value
            if word == "true" or word == "false":
                semanticMessage = f"Type 7 Error at '{item}': Use of reserved keyword in String"
            else:
                semanticMessage = "clear"
            return semanticMessage



        while True:
            returnMessage = "clear"
            isList = False
            for item in list:
                if isList:
                    returnMessage = type6check(item)
                    if returnMessage != "clear":
                        break
                if item.label == GrammarType.NUMBER:
                    returnMessage = type1check(item)
                    if returnMessage != "clear":
                        break
                    returnMessage = type3check(item)
                    if returnMessage != "clear":
                        break
                if item.label == GrammarType.PAIRSTRING:
                    returnMessage = type2check(item)
                    if returnMessage != "clear":
                        break
                    returnMessage = type4check(item)
                    if returnMessage != "clear":
                        break
                    returnMessage = type5check(item)
                    if returnMessage != "clear":
                        break
                    returnMessage = type7check(item)
                    if returnMessage != "clear":
                        break
                if item.label == GrammarType.STRING:
                    returnMessage = type7check(item)
                    if returnMessage != "clear":
                        break
                if item.label == GrammarType.LBRACK:
                    if isList == False:
                        isList = True
                    else:
                        continue
                if item.label == GrammarType.RBRACK:
                    listType.pop()
                    if len(listType) == 0:
                        isList = False
                    continue

                #remove this later
                else:
                    # returnMessage = "clear"
                    continue
            break
        return returnMessage
    def output(self, parseList):
        #turn parseList into a single array, through debugging I noticed that just printing out the array
        #would show two sets of square brackets at the start and end, indicating I had a nested array
        def clean(items):
            clean_list = []
            for item in items:
                #this checks to see if the item at the current index is another array within the array. if it is,
                #it calls clean again, in order to extract those items from that inner array
                if isinstance(item, list):
                    clean_list.extend(clean(item))
                else:
                    clean_list.append(item)
            return clean_list

        clean_list = list(clean(parseList))

        def pruneList(clean_list):
            pruneLocations = []
            #mark items that need to be removed from list
            for i in range(len(clean_list)):
                if clean_list[i].label == GrammarType.VALUE:
                    # clean_list.pop(i)
                    pruneLocations.append(i)
                elif clean_list[i].label == GrammarType.PAIR:
                    # clean_list.pop(i)
                    pruneLocations.append(i)
                elif clean_list[i].label == GrammarType.LIST:
                    # clean_list.pop(i)
                    pruneLocations.append(i)
                elif clean_list[i].label == GrammarType.DICT:
                    # clean_list.pop(i)
                    pruneLocations.append(i)

            #Remove the marked items
            for i in reversed(range(len(pruneLocations))):
                clean_list.pop(pruneLocations[i])

        pruneList(clean_list)
        semanticStatus = self.semanticCheck(clean_list)

        if semanticStatus != "clear":
            message = []
            message.append(semanticStatus)
            return message
        else:
            #this method is used to concatenate indentations before each output
            def indentor(indentAmount):
                return "\t" * indentAmount

           #finally, print out everything
            indentAmount = 0
            indentMin = []
            indentBrace = []
            counter = 0
            outputList = []
            #maybe add the new indentamount to a list, pop it once you get to a terminal. this may take care of
            #the case where there might be a list within a list?
            for item in clean_list:
                #this ensures the very first item in the array doesn't get indented
                if counter == 0:
                    print(repr(item))
                    outputList.append(repr(item))
                    indentBrace.append(0)
                    counter += 1

                elif item.label == "LBRACE" or item.label == "LBRACK":
                    indentAmount = indentBrace[-1] + 1
                    # indentMin.append(indentAmount)
                    indentBrace.append(indentAmount)
                    indents = indentor(indentBrace[-1])
                    print(indents + repr(item))
                    outputList.append(indents + repr(item))

                elif item.label == "COM":
                    indents = indentor(indentBrace[-1])
                    print(indents + repr(item))
                    outputList.append(indents + repr(item))

                elif item.label == "RBRACE" or item.label == "RBRACK":
                    indents = indentor(indentBrace.pop())
                    print(indents + repr(item))
                    outputList.append(indents + repr(item))

                elif item.label == "COL":
                    indents = indentor(indentBrace[-1]+1)
                    print(indents + repr(item))
                    outputList.append(indents + repr(item))
                    indentMin.append(indentBrace[-1]+1)

                #I have no idea why this has to be like this. I tried debugging for an hour and eventually
                #tried this... makes no sense why the others can just use a string comparison
                elif item.label == GrammarType.PAIRSTRING:
                    indents = indentor(indentBrace[-1]+1)
                    print(indents + repr(item))
                    outputList.append(indents + repr(item))

                elif (item.is_terminal == True):
                    indents = indentor(indentBrace[-1] + 1)
                    print(indents + repr(item))
                    outputList.append(indents + repr(item))

                else:
                    indents = indentor(indentBrace[-1] + 1)
                    print(indents + repr(item))
                    outputList.append(indents + repr(item))

            return outputList

    #this is essentially parse_value, as everything that a value consists of can be detected here
    def determineType(self):
                
        #skip if it's an empty token
        if self.current_token == "":
            return
            
        if "str" in self.current_token[:4]:
            return self.parse_String()
        
        if "int" in self.current_token[:4] or "float" in self.current_token[:6]:
            return self.parse_Num()
        
        if "null" in self.current_token[:5]:
            return self.parse_Null()
            
        if "lbrace" in self.current_token[:7]:
           return self.parse_Dict()

        if "bool" in self.current_token[:5]:
            return self.parse_Bool()
        
        if "lbrack" in self.current_token[:7]:
            return self.parse_List()
        
        else:
            errorValue = f"invalid token type: {self.current_token}"
            self.eatError.append(errorValue)
            self.errorLocation.append(self.position)
            self.hasError = True
        
    def parse_List(self):
        self.eat("[")
        returnValue = []
        returnValue.append(Grammar(GrammarType.LIST, "list", False))
        returnValue.append(Grammar(GrammarType.LBRACK, "[", True))
        token = self.determineType()
        returnValue.append(Grammar(GrammarType.VALUE, "value", False))
        returnValue.append(token)
        self.advance()
        
        while "rbrack" not in self.current_token[:7] and self.position < len(self.token_list)-2:
            if "com" in self.current_token[:4]:
                returnValue.append(Grammar(GrammarType.COM, ",", True))
                self.eat(",")
                if "lbrack" in self.current_token[:7]:
                    token = self.parse_List()
                elif "lbrace" in self.current_token[:7]:
                    token = self.determineType()
                else:
                    token = self.determineType()
                    self.advance()
                returnValue.append(Grammar(GrammarType.VALUE, "value", False))
                returnValue.extend(token)
            else:
                self.eat(",")
        self.eat("]")
        returnValue.append(Grammar(GrammarType.RBRACK, "]", True))
        return returnValue
        
    
    def parse_Bool(self):
        tempArr = []
        tempArr = self.current_token.split()
        returnValue = []
        # returnValue.append(Grammar(GrammarType.VALUE, "value", False))
        returnValue.append(Grammar(GrammarType.BOOL, tempArr[1].strip('">'), True))
        return returnValue

    def parse_String(self):
        returnValue = []
        # returnValue.append(Grammar(GrammarType.VALUE, "value", False))
        returnValue.append(Grammar(GrammarType.STRING, self.current_token[6:].strip('">'), True))
        return returnValue
    
    def parse_PairString(self):
        return Grammar(GrammarType.PAIRSTRING, self.current_token[6:].strip('">'), True)
    
    def parse_Num(self):
        tempArr = []
        tempArr = self.current_token.split()
        returnValue = []
        # returnValue.append(Grammar(GrammarType.VALUE, "value", False))
        returnValue.append(Grammar(GrammarType.NUMBER, tempArr[1].strip('>'), True))
        return returnValue
    
    def parse_Null(self):
        returnValue = []
        # returnValue.append(Grammar(GrammarType.VALUE, "value", False))
        returnValue.append(Grammar(GrammarType.NULL, True))
        return returnValue
    
    def parse_Dict(self):
        self.eat("{")
        returnValue = []
        returnValue.append(Grammar(GrammarType.DICT, "dict", False))
        returnValue.append(Grammar(GrammarType.LBRACE, "{", True))
        toString = self.determineType()
        #getting here and rbrace is the current token, and then self.advance() is called
        #check if this throws an error for mismatched braces
        if "str" in self.current_token:
            getpairs = self.parse_Pair()
            returnValue.append(getpairs)
            if "rbrace" in self.current_token[:7]:
                self.eat("}")
                returnValue.append(Grammar(GrammarType.RBRACE, "}", True))
                return returnValue
        self.advance()
        while "com" in self.current_token[:4] and "}" not in self.current_token and self.position < len(self.token_list)-2:
            returnValue.append(Grammar(GrammarType.COM, ",", True))
            self.eat(",")
            # toString = self.determineType()
            if "str" in self.current_token:
                getpairs = self.parse_Pair()
                returnValue.append(getpairs)
                self.advance()
        self.eat("}")
        returnValue.append(Grammar(GrammarType.RBRACE, "}", True))
        return returnValue
    
    def parse_Pair(self):
        returnValue = []
        returnValue.append(Grammar(GrammarType.PAIR, "pair", False))

        #make sure the first thing in the pair is a string
        if "str" in self.current_token:
            toString = self.parse_PairString()
            returnValue.append(toString)
            self.advance()
            #make sure the next token is a colon. then, advance, and find the value of that
            # <col, :> check index 6
            if "col" in self.current_token[:4]:
                returnValue.append(Grammar(GrammarType.COL, ":", True)) 
                self.eat(":")
                if "lbrack" in self.current_token[:7]:
                    returnValue.append(Grammar(GrammarType.VALUE, "value", False))
                    value = self.parse_List()
                    returnValue.append(value)
                elif "lbrace" in self.current_token[:7]:
                    returnValue.append(Grammar(GrammarType.VALUE, "value", False))
                    
                    value = self.parse_Dict()
                    returnValue.append(value)
                    
                else:
                    returnValue.append(Grammar(GrammarType.VALUE, "value", False))
                    value = self.determineType()
                    returnValue.append(value)
        return returnValue

        
if __name__ == "__main__":
    test_input = open(input('Type in the file name you would like to read in from\n'), "r").read()
    p = Parser(test_input)
    outputValues = p.parse()
    with open("parseroutput.txt", "w") as out:
        for item in outputValues:
            out.write(str(item) + "\n")