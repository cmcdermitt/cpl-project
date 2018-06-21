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
	'LET', 'REPEAT', 'UNTIL', 'ENDREPEAT', 'DISPLAY', 'IDENTIFIER', 'CNST_INT', 'CNST_FLOAT', 'CNST_STRING', '+', '-'], range(1,100)))

error = 0
currentId = 0
charNumber = 0
tokenNum = 0

def processAlphaOr_(line): #if the first character is alphabetic or the underscore 
	global charNumber
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
	lex_type = keywords.get(token) #give it the keyword's id
	if(lex_type == None):
		lex_type = keywords['IDENTIFIER'] #to be expanded later, will give identifiers individual ids
	
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
	

	lex_type = keywords['CNST_INT']
	
	
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
			lex_type = keywords['CNST_FLOAT']
	
	if(currentChar == 'e' and lex_type == cnst_float):
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
			return [token, eror]
						
	if(currentChar.isalpha()):
		lex_type = error
	return [token, lex_type]
	
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

	lex_type = keywords['CNST_STRING']
	if(currentChar != '\"'):
		lex_type = error	
	charNumber += 1
	return [token, lex_type]
	
def processArit(line):
	global charNumber
	currentChar = line[charNumber]
	token = currentChar
	charNumber += 1
	if(currentChar == '+' or currentChar == '-'):
		if(charNumber < len(line)):
			currentChar = line[charNumber]
			charNumber += 1
			if(currentChar == ' '):
				return [token, keywords[token]]
			elif(currentChar.isdigit()):
				val = processNumeric(line)
				val[0] = token + val[0]
				return val	
			
def processLine(line):
	if(len(line) == 0):
		return #if the line is empty, return
	global currentChar
	global charNumber
	global currentId
	charNumber = 0
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
			token =processArit(line) #Go down arithmetic path
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
