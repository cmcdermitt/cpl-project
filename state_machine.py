'''
Authors: Charlie McDermitt
         Eric Schneider
         Corey Harris
Class:   CS4308 - W01
         Concepts of Programming Languages
Title:   Final Project - Second Deliverable
Date:    09 July 2018
'''

import string
from enum import Enum

#list possible keywords and their ids
keywords = dict(zip([ 'IMPLEMENTATION',
	'MAIN', 'DESCRIPTION', 'PARAMETERS', 'OF', 'IDENTIFIER',
  	'VALUE', 'ARRAY', 'ICON',
   	'BAND', 'BOR', 'BXOR',
    'MOD', 'LSHIFT', 'RSHIFT', 'NEGATE', 'POINTER', 'STRUCT',
	'STRUCTYPE', 'ARRAY',
	'RETURN', '[empty]', 'FUNCTION', 'IS', 'BEGIN',
	'ENDFUN', 'PRECONDITION', 'MTRUE', 'MFALSE', 'CONSTANTS',
	'VARIABLES', 'DEFINE', 'NOT', 'AND', 'OR',
	'SET', 'READ', 'INPUT', 'DISPLAY', 'DISPLAYN',
	'MCLOSE', 'MOPEN', 'MFILE', 'INCREMENT', 'DECREMENT',
	'CALL', 'IF', 'THEN', 'ENDIF', 'FOR',
	'DO', 'ENDFOR', 'REPEAT', 'UNTIL', 'ENDREPEAT',
	'WHILE', 'ENDWHILE', 'CASE', 'MENDCASE', 'MBREAK',
	'MEXIT', 'POTCONDITION', 'ELSEIF', 'WRITE', 'TO',
	'FROM', 'DOWNTO', 'DEFAULT',
	'USING', 'MVOID', 'INTEGER', 'SHORT', 'REAL',
	'FLOAT', 'DOUBLE', 'TBOOL', 'CHAR', 'TSTRING',
	'LENGTH', 'TBYTE', 'TUNSIGNED', 'MTRUE', 'LETTER',
	'HCON', 'FCON', 'RELOP', 'OUTPUT', 'LB', 'RB'], range(1,120)))

identifiers = {}
identifier_id = 701
error = 0

charNumber = 0
tokenNum = 0

# Name processAlphaOr_
# Summary Processes part of a line under the condition that
# the current character is a letter or an underscore
# The function identifies the keyword or identifieier
# and returns the a string value and whether or not
# the value is a keyword or an identifier in a lists

def processAlphaOr_(line):
	global charNumber
	global identifier_id
	token = ''
	currentChar = line[charNumber] #mark current position in line
	#keep going until you have a character that isn't _ or alphanumeric
	while((currentChar.isalpha() or currentChar.isdigit() or currentChar == '_') and charNumber < len(line)):
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber]

	if token.upper() in keywords.keys(): #if the token is a keyword, give it the keyword's id
		lex_type = "KEYWORD"
		#lex_type = keywords.get(token.upper())
		anyAllowedAfter = False
		openParenthAllowed =  False
		closedBracketAllowed = False
	else: #it's an identifier
		anyAllowedAfter = False
		openParenthAllowed =  True
		closedBracketAllowed = True
		if token in identifiers.keys(): #if the identifier has already been used, look up its id
			lex_type = "IDENTIFIER"
			#lex_type = identifiers.get(token)
		else: #if it hasn't been used before, give it a new id
			identifiers[token] = identifier_id
			lex_type =  "IDENTIFIER"
			#lex_type = identifier_id
			identifier_id += 1

	if(currentChar == '?' or currentChar == '!'): #This list can be expanded later
		lex_type == error
	return [token, lex_type]

# Name processNumeric
# Summary Processes a line under the pcondition
# that the initial character is a digit. Digits are
# added to the value until a space or a decimal point
# is found. If a decimal point is found, then more Digits
# are seeked to complete the floating point number. Additionally,
# if the letter 'e' is found, then the optional values + or -
# followed by more digits are seeked to create a number in
# scientific notation
# If the character 'h' is found instead of the decimal points
# , or if the letters 'A', 'B', 'C', 'D', 'E', or 'F' are found,
# then the type is perceived to be hex; hex characters are then seeked
# until 'h' is found. The value of the number and the specific type
# are returned

def processNumeric(line):
	global charNumber
	anyAllowedAfter = False
	openParenthAllowed =  False
	closedBracketAllowed = True
	token = ''
	currentChar = line[charNumber]
	hexPossible = False
	if(currentChar == '0'):
		hexPossible = True
	# Go through the whole number part of the number (int or float)
	while(currentChar.isdigit() and charNumber < len(line)):
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber]

	#lex_type = types['INTEGER'] #set type to integer
	lex_type = "ICON"

	if(charNumber < len(line)):
		if(currentChar == 'h'): # Determine if a number is in hex; a hex number might not contain A,B,C,D,E or F
			if(hexPossible):
				closedBracketAllowed = False
				#lex_type = types['HEX_INTEGER']
				lex_type = "HCON"
				token += currentChar
				charNumber += 1
				return [token, lex_type]
			else:
				return [token, error]

		elif(currentChar == 'A' or currentChar == 'B' or currentChar == 'C' or currentChar == 'D' or currentChar == 'E' or currentChar == 'F'): # Add characters to hex number also determine if number is hex
			token += currentChar
			charNumber += 1
			if(charNumber < len(line)):
				currentChar = line[charNumber]
				while(charNumber < len(line) and (currentChar == 'A' or currentChar == 'B' or currentChar == 'C' or currentChar == 'D' or currentChar == 'E' or currentChar == 'F' or currentChar.isdigit())):
					token += currentChar
					charNumber += 1
					if(charNumber < len(line)):
						currentChar = line[charNumber]
			if(currentChar == 'h'): # Complete hex number with the character h
				token += currentChar
				charNumber+= 1
				closedBracketAllowed = False
				#lex_type = types['HEX_INTEGER']
				lex_type = "HCON"
				return [token, lex_type]
			else:
				return [token, error]



		elif(currentChar == '.'): # If there is a . character, the token is floating point.
			closedBracketAllowed = False
			token = token + currentChar
			charNumber += 1
			if(charNumber < len(line)): # Check that the floating point number continues
				currentChar = line[charNumber]
				while(currentChar.isdigit() and charNumber < len(line)): # Add the numbers after the decimal point to the token
					token = token + currentChar #add character to current token
					charNumber += 1	#increment
					if(charNumber < len(line)):
						currentChar = line[charNumber]
			#lex_type = types['REAL'] #mark the token as floating point
			lex_type = "FCON"

	#if(currentChar == 'e' and lex_type == types['REAL']): #if the next character is the beginning of an exponent
	if currentChar == 'e' and lex_type == "FCON":
		token += currentChar
		charNumber+= 1

		if(charNumber < len(line)):
			currentChar = line[charNumber]
			if(currentChar == '+' or currentChar == '-'): #if the next character is a sign, track it
				token += currentChar
				charNumber += 1
			if(charNumber < len(line)): #if there isn't a sign
				currentChar = line[charNumber]
				while(currentChar.isdigit() and charNumber < len(line)): #add all the digits to the token
					token = token + currentChar
					charNumber += 1
					if(charNumber < len(line)):
						currentChar = line[charNumber]
			else: #if there are no valid characters after the e or the sign, return an error code
				return [token, error]
		else: #if there are no valid characters after the e, return an error code
			return [token, error]

	if(currentChar.isalpha()): #return an error if there's a letter
		lex_type = error
	return [token, lex_type]

# Name processQuotes
# Summary: Processes a string at the index charNumber in a line_table
# Characters are appended to a value until a closing quotation mark is found.
# If a closing quotation mark is not found, then the type is error. Otherwise,
# the type is STRING. Finally, the value and the type are returned in a list.

def processQuotes(line): #if first character is "
	global charNumber
	anyAllowedAfter = False
	openParenthAllowed = True
	closedBracketAllowed = False
	currentChar = line[charNumber]
	token = currentChar

	charNumber += 1
	if(charNumber < len(line)):
		currentChar = line[charNumber] #move to the next character if there is one. Otherwise return an error.
	else:
		return [token, error]
	while(currentChar != '\"' and charNumber < len(line)): #while we haven't reached an end quote or the end of the line
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber] #move up

	#lex_type = types['STRING'] #set type to string
	lex_type = "STRING"
	if(currentChar != '\"'): #if the last character isn't a quotation mark, switch type to error instead
		lex_type = error
	charNumber += 1
	token += currentChar
	return [token, lex_type]


# Name processSingleQuote
# Summary Processes a single character.
#
#
#

def processSingleQuote(line): #if first character is '
	global charNumber
	currentChar = line[charNumber]
	token = currentChar

	#check whether there is another token
	charNumber += 1
	if charNumber < len(line):
		currentChar = line[charNumber]
	else:
		return [token, error]
	if currentChar.isalpha() or currentChar.isdigit(): #check whether the next token is alphanumeric (which is required for char)
		token = token + currentChar
		charNumber += 1

		#check whether there is another token
		if charNumber < len(line):
			currentChar = line[charNumber]
		else:
			return [token, error]
		if currentChar == '\'': #check whether there's an ending quote, return the char if so, otherwise error
			token = token + currentChar
			#lexType = types['CHAR']
			lexType = "LETTER"
			charNumber += 1
			return [token, lexType]
		else:
			return [token, error]
	else: #if the character after the ' isn't alphanumeric, it's an error
		return [token, error]

# Name processLine
# Summary Takes an input line and checks the current character.
# Depending on the current character, a function is called which
# moves the index of the current character and returns a lexeme
# Once all of the lexemes are collected in a list, the list is returned

def processLine(line):
	if(len(line) == 0):
		return #if the line is empty, return
	global currentChar
	global charNumber
	anyAllowedAfter = True
	openParenthAllowed = True
	bracketAllowed = True
	charNumber = 0
	token = []
	line_table = []
	processedToken = False

	while(charNumber < len(line)):
		currentChar = line[charNumber]
		if(line[charNumber].isalpha() or line[charNumber] == '_'):
			if(not anyAllowedAfter):
				return [token, 0]
			token = processAlphaOr_(line) # Go down the underscore or alpha path
			processedToken = True
		elif(line[charNumber].isdigit()):
			if(not anyAllowedAfter):
				return [token, 0]
			token = processNumeric(line) # Go down the number
			processedToken = True
		elif(line[charNumber] == '\"'): # Go down the quotation path
			if(not anyAllowedAfter):
				return [token, 0]
			token = processQuotes(line)
			processedToken = True
		elif(line[charNumber] == '\''):
			if(not anyAllowedAfter):
				return [token, 0]
			token = processSingleQuote(line)
			processedToken  = True
		else:
			anyAllowedAfter = True
			openParenthAllowed =  True
			bracketAllowed =  True	#Get next character
			charNumber += 1

		if(processedToken): #once we've processed a token
			if (token[1] == 0): #if it's an error, just return that token - the line is invalid anyway and this makes it easier to keep track of errors.
				return [token, 0]
			line_table.append(token) #add the processed token to a line
			processedToken = False #get ready for a new token

	return line_table #return a list of lists, where each sublist represents one token in the line
