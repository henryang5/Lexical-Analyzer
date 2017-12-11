"""
Henry Ang
CSC 3310 Concepts in Programming Language
11/1/17
Python programming assignment

Write a program in Python that takes a program written in Mini – Pascal, and outputs the lexemes and
lexemes into a new file.

<constant> ::=	<integer constant> | <character constant> | <constant identifier>
<constant identifier> ::=	<identifier>
<identifier> ::=	<letter> { <letter or digit> }
<letter or digit> ::=	<letter> | <digit>
<integer constant> ::=	<digit> { <digit> }
<character constant> ::=	'< any character other than ' >'  |  ''''
<letter> ::=	a | b | c | d | e | f | g | h | i | j | k | l | m | n | o |
p | q | r | s | t | u | v | w | x | y | z | A | B | C |
D | E | F | G | H | I | J | K | L | M | N | O | P
| Q | R | S | T | W | V | W | X | Y | Z
<digit> ::=	0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<special symbol> ::=	+ | - | * | = | <> | < | > | <= | >= |
( | ) | [ | ] | := | . | , | ; | : | .. | div | or |
and | not | if | then | else | of | while | do |
begin | end | read | write | var | array |
procedure | program
<predefined identifier> ::=	integer | Boolean | true | false
"""

from __future__ import print_function
import re
import sys

def getLex():

    numTokens = 0
    quoteCount = 0
    token = ''
    inputFile = ""
    chars = []
    lexemes = []
    tokens = []
    id = []
    values = []

    try:                                                     # try-except to check if input is invalid
        if(len(sys.argv) != 2):
            print("Invalid input. Enter: python filename inputfile")
            quit()
        else:
            inputFile = sys.argv[1]
        # inputFile = str(input('Enter a input file name: '))  # ask user to input a input fileNames
        print("Processing input file: " + inputFile)
        with open(inputFile, "r") as file:                   # reads input file
            for line in file:                                # reads file by line
                for char in line:                            # read character by line
                    chars.append(char)
    except (FileNotFoundError, IOError, ValueError):     # invalid fileNames or File not found
        print("File not found.")
        quit()

    # create lexemes from characters
    for char in chars:
        if (isLetter(char)):
            token += char
            if (isSpecialSym(token)):
                lexemes.append(token)
                token = ''
                numTokens += 1
        elif (isDigit(char)):
            token += char
        elif ((char == "+") | (char == "-") | (char == "*") | (char == "<") | (char == ">") |
             (char == "=") | (char == ".") | (char == ",") | (char == ":")):
            lexemes.append(char)
            numTokens += 1
        elif(isID(token)):
            lexemes.append(token)
            token = ''
            numTokens += 1
        elif (char == ";"):
            if (isID(token)):
                lexemes.append(token)
                token = ''
                numTokens += 1
            elif (isIntConst(token)):
                lexemes.append(token)
                token = ''
                numTokens += 1
            lexemes.append(char)
            numTokens += 1
        elif ((char == ('\''))):
            token += char
            quoteCount += 1
            if(quoteCount == 2):
                quoteCount = 0
                lexemes.append(token)
                token = ''
                numTokens += 1
        elif (char ==  ' '):
            if quoteCount == 1:
                token += char
        elif(isString(token)):
            lexemes.append(token)
            token = ''
            numTokens += 1
        elif(isSpecialSym(token)):
            lexemes.append(token)
            token = ''
            numTokens += 1

    # puts id values in id list
    for token in lexemes:
        if(isSpecialSym(token)):
            id.append(token)
        elif(isPreID(token)):
            id.append(token)
        elif(isID(token)):
            id.append(token)
        else:
           id.append("")

        # create tokens, and value lists
        if(isPreID(token)):
            tokens.append("PRE_ID")
            values.append("")
        elif (isIntConst(token)):
            tokens.append("INT_CONST")
            values.append(token)
        elif (isString(token)):
            tokens.append("CHAR_CONST")
            string = token.strip("\'")
            values.append(string)
        elif(token == ";"):
            tokens.append("SEMICOLON")
            values.append("")
        elif (token == "+"):
            tokens.append("PLUS")
            values.append("")
        elif (token == "-"):
            tokens.append("MINUS")
            values.append("")
        elif (token == "*"):
            tokens.append("TIMES")
            values.append("")
        elif (token == "="):
            tokens.append("ASSIGNS")
            values.append("")
        elif (isSpecialSym(token)):
            tokens.append("SPEC_SYM")
            values.append("")
        elif (isID(token)):
            tokens.append("ID")
            values.append("")
        else:
            print(token + " not found in mini-pascal grammar")
            quit()

    # print(chars)
    # print(lexemes)
    # print(id)
    # print(tokens)
    # print(values)

    print(str(numTokens) + " tokens produced")

    # create outputfile
    inFileName = inputFile.replace(' ', "")[:-4]
    outFile = inFileName + ".out"
    try:
        with open(str(outFile), 'w') as outputfile:  # create output file
        # prints to output file
            for i in range(0, numTokens, 1):
                print("{0:<10} {1:<8} {2:<6}".format(tokens[i], id[i], values[i]), file=outputfile)
        outputfile.close()
        print("Resuts in file " + outFile)
    except(IndexError):
        print("Error found in Grammar")
        quit()

def isLetter(char):
    letter = re.match("[a-zA-Z]", char)
    return letter

def isDigit(char):
    digit = re.match("[0-9]", char)
    return digit

def isID(token):
    id = re.match("[a-zA-Z]([a-zA-Z]|[0-9])*", token)
    return id

def isString(token):
    string = re.match("\'([^\'\'\'\'])*\'", token)
    return string

def isIntConst(token):
    intConst = re.match("[0-9][0-9]*", token)
    return intConst

def isSpecialSym(token):
    isSpecialSym = re.match("([+|-|*|=|<>|<|>|<=|>=|(|)|[|]|:=|[.]|,|;|:|[..]|div|or|"
                            "and|not|if|then|of|while|do|begin|end|read|write|var|array|program|procedure])", token)
    return isSpecialSym

def isPreID(token):
    isPreID = re.match("(integer|Boolean|true|false)", token)
    return isPreID

def main():
    """
    Main function of the program.
    """
    print('Welcome to Lexer Generator, written by Henry Ang.')
    getLex()

if __name__ == "__main__":
    main()

