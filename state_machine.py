#Move all of this to Scanner.py later 
import string
from enum import Enum

#list possible keywords and their ids
keywords = dict(zip(['(', ')', '[', ']', 'IMPLEMENTATION',
	'MAIN', 'DESCRIPTION', 'PARAMETERS', 'OF', 'IDENTIFIER',
  	'VALUE', 'ARRAY', 'ICON', '+', '-',
   	'BAND', 'BOR', 'BXOR', '*', '/',
    'MOD', 'LSHIFT', 'RSHIFT', 'NEGATE', ',',
	':=', 'POINTER', 'STRUCT', 'STRUCTYPE', 'ARRAY',
	'RETURN', '[empty]', 'FUNCTION', 'IS', 'BEGIN',
	'ENDFUN', 'PRECONDITION', 'MTRUE', 'MFALSE', 'CONSTANTS',
	'VARIABLES', 'DEFINE', 'NOT', 'AND', 'OR',
	'SET', 'READ', 'INPUT', 'DISPLAY', 'DISPLAYN',
	'MCLOSE', 'MOPEN', 'MFILE', 'INCREMENT', 'DECREMENT',
	'CALL', 'IF', 'THEN', 'ENDIF', 'FOR',
	'DO', 'ENDFOR', 'REPEAT', 'UNTIL', 'ENDREPEAT',
	'WHILE', 'ENDWHILE', 'CASE', 'MENDCASE', 'MBREAK',
	'MEXIT', 'POTCONDITION', 'ELSEIF', 'WRITE', 'TO',
	'FROM', ':', '.', 'DOWNTO', 'DEFAULT',
	'USING', 'MVOID', 'INTEGER', 'SHORT', 'REAL',
	'FLOAT', 'DOUBLE', 'TBOOL', 'CHAR', 'TSTRING',
	'LENGTH', 'TBYTE', 'TUNSIGNED', 'MTRUE', 'LETTER',
	'HCON', 'FCON', 'RELOP', '==', '>', 
	'<', '>=', '<=', 'OUTPUT'], range(1,120)))

#
types = dict(zip(['INTEGER', 'SIGNED_INTEGER', 'HEX_INTEGER', 'REAL', 'SIGNED_REAL', 'CHAR', 'STRING',
 	'CONST_INTEGER', 'CONST_SIGNED_INTEGER', 'CONST_HEX_INTEGER', 'CONST_REAL', 'CONST_SIGNED_REAL', 'CONST_CHAR', 'CONST_STRING'], range(501, 520)))

#dictionary of characters used for grouping
grouping_characters = dict(zip(['(', ')', '[', ']', '{', '}'], range(601,606)))

#list which characters are parts of operators
operator_characters = ['+', '-', '*', '/', '=', ':', '<', '>', ',']
#list types and their possible ids

identifiers = {}
identifier_id = 701
error = 0

currentId = 0
charNumber = 0
tokenNum = 0
anyAllowedAfter = True
spaceRequired = True
openParenthAllowed = True

def processAlphaOr_(line): #if the first character is alphabetic or the underscore 
	global charNumber
	global identifier_id
	token = ''
	currentChar = line[charNumber] #mark current position in line
	global anyAllowedAfter 
	global openParenthAllowed 
	global closedBracketAllowed 
	#keep going until you have a character that isn't _ or alphanumeric
	while((currentChar.isalpha() or currentChar.isdigit() or currentChar == '_') and charNumber < len(line)):
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber]
	
	'''if(charNumber < len(line)):	#for nonalphanumeric characters that aren't the end of the line
		if(line[charNumber] == '+' or line[charNumber] == '-' or line[charNumber] == '*' or
		line[charNumber] == '/' or line[charNumber] == '%'): #if it's an arithmetic operator
			charNumber = charNumber - 1 #Back up for arithmetic operators'''
	
	if(currentChar == "."): #if there's a dot operator, store the second half of the identifier
		if(charNumber < len(line)):
			token = token + currentChar
			charNumber += 1
			currentChar = line[charNumber]
			if(charNumber >= len(line)):
				return [token, error]
			else:
				while((currentChar.isalpha() or currentChar.isdigit() or currentChar == '_') and charNumber < len(line)):
					token = token + currentChar #add character to current token
					charNumber += 1	#increment
					if(charNumber < len(line)):
						currentChar = line[charNumber]
	elif(currentChar == '-'): #if there's a hyphen, check whether it's part of an arrow operator
		charNumber+= 1
		token += currentChar
		if(charNumber < len(line)):
			currentChar = line[charNumber]
			if(currentChar == '>'): #if there's an arrow operator, store the rest of the identifier. Otherwise it's an error.
				token += currentChar
				charNumber += 1
				currentChar = line[charNumber]
				if(charNumber >= len(line)):
					return [token, error]
				else:
					while((currentChar.isalpha() or currentChar.isdigit() or currentChar == '_') and charNumber < len(line)):
						token = token + currentChar #add character to current token
						charNumber += 1	#increment
						if(charNumber < len(line)):
							currentChar = line[charNumber]
			else:
				return [token, error]

	if token.upper() in keywords.keys(): #if the token is a keyword, give it the keyword's id
		lex_type = keywords.get(token.upper())
		anyAllowedAfter = False
		openParenthAllowed =  False
		closedBracketAllowed = False
	else: #it's an identifier
		anyAllowedAfter = False
		openParenthAllowed =  True
		closedBracketAllowed = True
		if token in identifiers.keys(): #if the identifier has already been used, look up its id
			lex_type = identifiers.get(token)
		else: #if it hasn't been used before, give it a new id
			lex_type = identifier_id
			identifier_id += 1
	
	if(currentChar == '?' or currentChar == '!'): #This list can be expanded later
		lex_type == error
	return [token, lex_type]

def processNumeric(line):
	global charNumber
	global anyAllowedAfter 
	global openParenthAllowed 
	global closedBracketAllowed 
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
	

	lex_type = types['INTEGER'] #set type to integer
	
	
	if(charNumber < len(line)):
		
		if(currentChar == 'h'):
			if(hexPossible):
				closedBracketAllowed = False
				lex_type = types['HEX_INTEGER']
				token += currentChar
				charNumber += 1
				return [token, lex_type]
			else:
				return [token, error] 
		
		elif(currentChar == 'A' or currentChar == 'B' or currentChar == 'C' or currentChar == 'D' or currentChar == 'E' or currentChar == 'F'):
			token += currentChar
			charNumber += 1
			if(charNumber < len(line)):
				currentChar = line[charNumber]
				while(charNumber < len(line) and (currentChar == 'A' or currentChar == 'B' or currentChar == 'C' or currentChar == 'D' or currentChar == 'E' or currentChar == 'F' or currentChar.isdigit())):
					token += currentChar
					charNumber += 1
					if(charNumber < len(line)):
						currentChar = line[charNumber]
			if(currentChar == 'h'):
				token += currentChar
				charNumber+= 1
				closedBracketAllowed = False
				lex_type = types['HEX_INTEGER']
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
			lex_type = types['REAL'] #mark the token as floating point
	
	if(currentChar == 'e' and lex_type == types['REAL']): #if the next character is the beginning of an exponent
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

	# Quotes needs support for in string quotation marks.
def processQuotes(line): #if first character is "
	global charNumber
	global anyAllowedAfter 
	global openParenthAllowed 
	global closedBracketAllowed
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

	lex_type = types['STRING'] #set type to string
	if(currentChar != '\"'): #if the last character isn't a quotation mark, switch type to error instead
		lex_type = error	
	charNumber += 1
	return [token, lex_type]

def processSingleQuote(line): #if first character is '
	global charNumber
	global anyAllowedAfter 
	global openParenthAllowed 
	global closedBracketAllowed
	anyAllowedAfter = False
	openParenthAllowed = False
	closedBracketAllowed = False
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
			lexType = types['CHAR']
			charNumber += 1
			return [token, lexType]
		else:
			return [token, error]
	else: #if the character after the ' isn't alphanumeric, it's an error
		return [token, error]
	
def processOperator(line):
	global charNumber
	global anyAllowedAfter 
	global openParenthAllowed 
	global closedBracketAllowed
	anyAllowedAfter = False
	openParenthAllowed = False
	closedBracketAllowed = False
	currentChar = line[charNumber]
	token = currentChar
	charNumber += 1

	if currentChar == '+' or currentChar == '-': #these two can be part of signed numbers
		currentChar = line[charNumber]

		if(currentChar.isdigit()): #if the next character's a digit, it's a signed number
			val = processNumeric(line) #process the number
			val[0] = token + val[0] #add the sign to the processed number
			val[1] = val[1] + 1 #since the ID of signed numbers (both ints and floats) is 1 more than the id of unsigned numbers, we can just add 1
			return val
		elif currentChar != ' ':
			openParenthAllowed = True
			return [token, token, 0] #error if the next character isn't a number or space

	elif currentChar != '*' and currentChar != '/': #if it's one of these we can just return
		openParenthAllowed = True
		if charNumber < len(line):
			nextChar = line[charNumber]
			if (currentChar + nextChar in keywords.keys()): #if the next two characters combined form a keyword
				token = currentChar + nextChar #return that
			elif currentChar not in keywords.keys(): #check if this one character is a keyword
				return [token, token, 0] #error if it isn't, otherwise return it
		else:
			if currentChar not in keywords.keys(): #check if this one character is a keyword
				return [token, token, 0] #error if it isn't, otherwise return it
				
	return [token, token, keywords[token]]

def processGrouping(line):
	global charNumber
	global identifier_id
	global anyAllowedAfter 
	global openParenthAllowed 
	global closedBracketAllowed
	anyAllowedAfter = False
	openParenthAllowed = True
	closedBracketAllowed = False
	currentChar = line[charNumber]
	token = currentChar
	processToken = []
	charNumber += 1

	#Check for parentheses, curly braces, or opening square bracket return token
	if(currentChar == '(' or currentChar == ')' or currentChar == '{' or currentChar == '}' or currentChar == '['):
		token = currentChar
		return [token, grouping_characters[token]]
	#currentChar is a closing sqaure bracket.
	#Keep scanning until space to catch all components of a indexing operation
	else:
		token = currentChar
		while(charNumber < len(line)):
			nextChar = line[charNumber]
			if(nextChar == " "): #end of line reached
				return [token, grouping_characters[token]]
			elif (nextChar == '(' or nextChar == ')' or nextChar == '[' or nextChar == ']'):
				currentChar = nextChar
				token = token + currentChar
			elif(nextChar == "."): #next character is dot operator. add to token
				currentChar = nextChar
				token = token + currentChar
				if(charNumber + 1 >= len(line)):
					return [token,error]
			elif(nextChar.isalpha() or nextChar == "_"): #Catch letter or underscore parts of identifier
				currentChar = nextChar
				token = token + currentChar
			elif(nextChar.isdigit()):
				token = token + nextChar
				if(currentChar == "."): #digit follows a letter
					return [token, error]
				currentChar = nextChar
			charNumber += 1

	if token in identifiers.keys(): #if the identifier has already been used, look up its id
		lex_type = identifiers.get(token)
	else: #if it hasn't been used before, give it a new id
		lex_type = identifier_id
		identifier_id += 1
		return [token, lex_type]


def processLine(line):
	if(len(line) == 0):
		return #if the line is empty, return
	global currentChar
	global charNumber
	global currentId
	global anyAllowedAfter 
	global openParenthAllowed 
	global closedBracketAllowed
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
		elif(line[charNumber] == '\"'):
			if(not anyAllowedAfter):
				return [token, 0]
			token = processQuotes(line)
			processedToken = True
		elif(line[charNumber] == '\''):
			if(not anyAllowedAfter):
				return [token, 0]
			token = processSingleQuote(line)
			processedToken  = True
		elif(line[charNumber] in operator_characters): # if it's an operator
			if(not anyAllowedAfter):
				return [token, 0]
			token = processOperator(line) #Go down operator path
			processedToken = True
		elif(line[charNumber] in grouping_characters): # if character is a brace, bracket, or parenthesis
			if(currentChar == ']' and not closedBracketAllowed):
				return [token, 0]
			if(currentChar == '(' and not openParenthAllowed):
				return [token, 0]
			token = processGrouping(line) #Go down grouping path
			processedToken = True
		else:
			anyAllowedAfter = True
			openParenthAllowed =  True
			bracketAllowed =  True	#Get next character
			charNumber += 1
		
		if(processedToken): #once we've processed a token
			if (token[1] == 0): #if it's an error, just return that token - the line is invalid anyway and this makes it easier to keep track of errors.
				return [token, 0]
			token.insert(0,currentId) #add the token's id - fix this later?
			line_table.append(token) #add the processed token to a line
			currentId = currentId + 1
			processedToken = False #get ready for a new token
		
	return line_table #return a list of lists, where each sublist represents one token in the line
