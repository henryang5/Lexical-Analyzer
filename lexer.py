"""
Henry Ang
CSC 3310 Concepts in Programming Language
11/1/17
Python programming assignment

Write a program in Python that takes a program written in Mini - Power, and outputs the lexemes and
lexemes into a new file.

"""

from __future__ import print_function
import re
import sys

def getLex():
    numTokens = 0
    quoteCount = 0
    token = ""
    inputFile = ""
    chars = []
    lexemes = []
    tokens = []
    id = []
    values = []
    lineCount = 0

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
                lineCount += 1
                for char in line:                            # read character by line
                    chars.append(char)
    except (FileNotFoundError, IOError, ValueError):     # invalid fileNames or File not found
        print("File not found.")
        quit()

    # create lexemes from characters
    for char in chars:
        if(isDigit(char)):
            token += char
        if(char == ";"):
            if(isRealConst(token)):
                lexemes.append(token)
                token = ""
                numTokens += 1
            if(isIntConst(token)):
                lexemes.append(token)
                token = ""
                numTokens += 1
        if (char == "=") | (char == "^") | (char == "+") | (char == "-") | (char == "*") | (char == "/"):
            lexemes.append(char)
            numTokens += 1
        if (char == ";"):
            lexemes.append(char)
            numTokens += 1
        if (char == ('(')):
            token += char
            lexemes.append(token)
            token = ""
            numTokens += 1
        if ((char == ('\"'))):
            token += char
            quoteCount += 1
            if(quoteCount == 2):
                quoteCount = 0
        if (char ==  ' '):
            if quoteCount == 1:
                token += char
        if (isString(token)):
            lexemes.append(token)
            token = ""
            numTokens += 1
        if (isLetter(char)):
            token += char
        if (char == "P") | (char == "R") | (char == "I") | (char == "N") | (char == "."):
            token += char
        if (char == "#") | (char == "$") | (char == "%") | (char == "T") | (char == (')')):
            token += char
            lexemes.append(token)
            token = ""
            numTokens += 1
        # check for invalid characters
        if ((char != "#") & (char != "$") & (char != "%") & (char != "T") & (char != (')')) &
                (char != "P") & (char != "R") & (char != "I") & (char != "N") & (char != ".") &
                (char != ' ') & (char != '\"') & (char != '(') & (char != ';') &
                (char != "=") & (char != "^") & (char != "+") & (char != "-") & (char != "*") & (char != "/")
                & (isDigit(char) is None)
                & (isLetter(char) is None) & (char != '\n')):
            print(char + " not found in Mini-Power grammar")
            quit()

    # puts id values in id list
    for token in lexemes:
        if(isID(token)):
            idVal = token.strip("$#%")
            id.append(idVal)
        else:
           id.append("")

        # create tokens, and value lists
        if(isID(token)):
            tokens.append("ID")
            sym = token.strip("abcdefghijklmnopqrstuvwxyz")
            if(sym == "%"):
                values.append("REAL")
            elif(sym == "#"):
                values.append("INTEGER")
            else:
                values.append("STRING")
        elif(token == "="):
            tokens.append("ASSIGN")
            values.append("")
        elif(isRealConst(token)):
            tokens.append("REAL_CONST")
            values.append(token)
        elif (isIntConst(token)):
            tokens.append("INT_CONST")
            values.append(token)
        elif (isString(token)):
            tokens.append("STRING")
            string = token.strip("\"")
            values.append(string)
        elif(token == ";"):
            if (lineCount == 1):
                print("Error - SemiColon on last line")
                quit()
            else:
                lineCount -= 1
                tokens.append("SEMICOLON")
                values.append("")
        elif (token == "PRINT"):
            tokens.append(token)
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
        elif (token == "/"):
            tokens.append("DIV")
            values.append("")
        elif (token == "^"):
            tokens.append("POWER")
            values.append("")
        elif (token == "("):
            tokens.append("LPAREN")
            values.append("")
        elif (token == ")"):
            tokens.append("RPAREN")
            values.append("")
        else:
            print(token + " not found in mini-power grammar")
            quit()
    if(lineCount != 1):
        print("Error: Semi-Colon missing")
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
    letter = re.match("[a-z]", char)
    return letter

def isDigit(char):
    digit = re.match("[0-9]", char)
    return digit

def isID(token):
    id = re.match("[a-z]([a-z]|[0-9])*[#|%|\$]", token)
    return id

def isString(token):
    string = re.match("^\"([a-z]|[0-9]|[\s])+\"$", token)
    return string

def isIntConst(token):
    intConst = re.match("[0-9][0-9]*", token)
    return intConst

def isRealConst(token):
    realConst = re.match("([+|-]*[0-9]+[.][0-9]+)", token)
    return realConst

def main():
    """
    Main function of the program.
    """
    print('Welcome to Lexer Generator, written by Henry Ang.')
    getLex()

if __name__ == "__main__":
    main()

