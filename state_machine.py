#Move all of this to Scanner.py later 
import string
keywords = dict(zip(['token', 'IDENTIFIER', 'HCON', 'FORWARD', 'REFERENCES',
	'MEXTERN', 'FUNCTION', 'MAIN', 'RETURN', 'POINTER', 'ARRAY', 'LB', 'RB','ICON',
	'TYPE', 'STRUCT', 'STRUCTYPE', 'MVOID', 'INTEGER',
	'SHORT', 'REAL', 'FLOAT', 'DOUBLE', 'TBOOL',
	'CHAR', 'TSTRING', 'OF', 'LENGTH', 'ICON',
	'TBYTE', 'SPECIFICATIONS', 'ENUM', 'STRUCT', 'GLOBAL',
	'DECLARATIONS', 'IMPLEMENTATIONS', 'FUNCTION', 'MAIN', 'PARAMETERS',
	'COMMA', 'CONSTANT', 'BEGIN', 'ENDFUN', 'IF',
	'THEN', 'ELSE', 'ENDIF', 'WHILE', 'ENDWHILE',
	'LET', 'REPEAT', 'UNTIL', 'ENDREPEAT', 'DISPLAY'], range(0,50)))

identifier = 51
cnst_int = 52
cnst_float = 53
cnst_string = 54	
currentId = 0
charNumber = 0
tokenNum = 0

def processAlphaOr_(line): #if the first character is alphabetic or the underscore
	global charNumber
	global identifier 
	token = ''
	currentChar = line[charNumber] #mark current position in line

	#keep going until you have a character that isn't _ or alphanumeric
	while((currentChar.isalpha() or currentChar.isdigit() or currentChar == '_') and charNumber < len(line)):
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber]
	
	if(charNumber < len(line)):	#for nonalphanumeric characters that aren't the end of the line
		if(line[charNumber] == '+' or line[charNumber] == '-' or line[charNumber] == '*' or
		line[charNumber] == '/' or line[charNumber] == '%'): #if it's an arithmetic operator
			charNumber = charNumber - 1 #Back up for arithmetic operators
	
	#print(type(token))
	lex_type = keywords.get(token.upper()) #give it the keyword's id
	if(lex_type == None):
		lex_type = identifier #to be expanded later, will give identifiers individual ids
	
	if(currentChar == '?' or currentChar == '!'): #This list can be expanded later
		return "error"
	return [token, lex_type]

def processNumeric(line):
	global charNumber
	global cnst_int
	global cnst_float
	
	token = ''
	currentChar = line[charNumber]
	
	# Go through the whole number part of the number (int or float)
	while(currentChar.isdigit() and charNumber < len(line)):
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber]
	

	lex_type = cnst_int
	
	
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
		lex_type = cnst_float
	if(currentChar.isalpha()):
		return "error"
	return [token, lex_type]
	
def processQuotes(line):
	global charNumber
	global cnst_string
	currentChar = line[charNumber]
	token = ''
	while(currentChar != '"\"' and charNumber < len(line)):
		token = token + currentChar #add character to current token
		charNumber += 1	#increment
		if(charNumber < len(line)):
			currentChar = line[charNumber]
	if(currentChar != '\"'):
		return "error"
	lex_type = cnst_string
	return [token, lex_type]
	

				
def processLine(line):
	if(len(line) == 0):
		return #if the line is empty, return
	global currentId
	global charNumber
	global tokenNum
	charNumber = 0
	tokenNum = 0
	currentChar = line[0]
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
		elif(line[charNumber] == '+' or line[charNumber] == '-' or line[charNumber] == '*' or
		line[charNumber] == '/' or line[charNumber] == '%'): # need to add <, >, etc
			x = 2 #Go down arithmetic path
		else:
			x = 2	#Get next character
			charNumber += 1
		if(processedToken):
			if (token == "error"):
				return token
			token.insert(0,tokenNum)
			token.insert(0,currentId)
			line_table.append(token)
			tokenNum = tokenNum + 1
			currentId = currentId + 1
			processedToken = False
		
	return line_table	
