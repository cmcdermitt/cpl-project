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

#list which characters are parts of operators
operator_characters = ['+', '-', '*', '/', '=', ':', '<', '>']

#list types and their possible ids

identifiers = {}
identifier_id = 501
error = 0

currentId = 0
charNumber = 0
tokenNum = 0

def processAlphaOr_(line): #if the first character is alphabetic or the underscore 
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
	
	'''if(charNumber < len(line)):	#for nonalphanumeric characters that aren't the end of the line
		if(line[charNumber] == '+' or line[charNumber] == '-' or line[charNumber] == '*' or
		line[charNumber] == '/' or line[charNumber] == '%'): #if it's an arithmetic operator
			charNumber = charNumber - 1 #Back up for arithmetic operators'''
	
	if(currentChar == "."):
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
	elif(currentChar == '-'):
		charNumber+= 1
		token += currentChar
		if(charNumber < len(line)):
			currentChar = line[charNumber]
			if(currentChar == '>'):
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
	
	#print(type(token))

	if token in keywords.keys(): #if the token is a keyword, give it the keyword's id
		lex_type = keywords.get(token)
	else: #it's an identifier
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
	token = ''
	currentChar = line[charNumber]
	
	# Go through the whole number part of the number (int or float)
	while(currentChar.isdigit() and charNumber < len(line)):
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber]
	

	lex_type = types['INTEGER']
	
	
	if(charNumber < len(line)):
		if(currentChar == '.'): # If there is a . character, the token is floating point. 
			token = token + currentChar
			charNumber += 1
			if(charNumber < len(line)): # Check that the floating point number continues
				currentChar = line[charNumber]
				while(currentChar.isdigit() and charNumber < len(line)): # Add the numbers after the decimal point to the token
					token = token + currentChar #add character to current token
					charNumber += 1	#increment
					if(charNumber < len(line)):
						currentChar = line[charNumber]
			lex_type = types['REAL']
	
	if(currentChar == 'e' and lex_type == types['REAL']):
		token += currentChar
		charNumber+= 1
		if(charNumber < len(line)):
			currentChar = line[charNumber]
			if(currentChar == '+' or currentChar == '-'):
				token += currentChar
				charNumber += 1
			if(charNumber < len(line)):
				currentChar = line[charNumber]
				while(currentChar.isdigit() and charNumber < len(line)):
					token = token + currentChar
					charNumber += 1
					if(charNumber < len(line)):
						currentChar = line[charNumber]
			else:
				return [token, error]
		else:
			return [token, error]
						
	if(currentChar.isalpha()):
		lex_type = error
	return [token, lex_type]

	# Quotes needs support for in string quotation marks.
def processQuotes(line): #if first character is "
	global charNumber
	currentChar = line[charNumber]
	token = ''

	charNumber += 1
	if(charNumber < len(line)):
		currentChar = line[charNumber]
	else:
		return [token, error]
	while(currentChar != '\"' and charNumber < len(line)): #while we haven't reached an end quote or the end of the line
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber] #move up

	lex_type = types['STRING']
	if(currentChar != '\"'):
		lex_type = error	
	charNumber += 1
	return [token, lex_type]
	
def processOperator(line):
	global charNumber
	currentChar = line[charNumber]
	token = currentChar
	charNumber += 1

	if currentChar == '+' or currentChar == '-':
		currentChar = line[charNumber]

		if(currentChar.isdigit()): #if the next character's a digit, it's a signed number
			val = processNumeric(line) #process the number
			val[0] = token + val[0] #add the sign to the processed number
			val[1] = val[1] + 1 #since the ID of signed numbers (both ints and floats) is 1 more than the id of unsigned numbers, we can just add 1
			return val
		elif currentChar != ' ':
			return [token, token, 0] #error if the next character isn't a number or space

	elif currentChar != '*' and currentChar != '/': #if it's one of these we can just return
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
				
			
def processLine(line):
	if(len(line) == 0):
		return #if the line is empty, return
	global currentChar
	global charNumber
	global currentId
	charNumber = 0
	#currentChar = line[0]
	token = []
	line_table = []
	processedToken = False
	while(charNumber < len(line)):
		if(line[charNumber].isalpha() or line[charNumber] == '_'):
			token = processAlphaOr_(line) # Go down the underscore or alpha path
			processedToken = True
		elif(line[charNumber].isdigit()):
			token = processNumeric(line) # Go down the underscore or alpha path
			processedToken = True
		elif(line[charNumber] == '\"'):
			token = processQuotes(line)
			processedToken = True
		elif(line[charNumber] in operator_characters): # if it's an operator
			token = processOperator(line) #Go down operator path
			processedToken = True
		else:
			x = 2	#Get next character
			charNumber += 1
		if(processedToken):
			if (token[1] == 0):
				return [token, 0]
			token.insert(0,currentId)
			line_table.append(token)
			currentId = currentId + 1
			processedToken = False
		
	return line_table	
