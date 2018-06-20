#Move all of this to Scanner.py later 

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

charNumber = 0
tokenNum = 0

def processAlphaOr_(line): #if the first character is alphabetic or the underscore
	global charNumber
	global tokenNum

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
	
	if(token in keywords.keys()): #if the token is a keyword
		id = keywords[token] #give it the keyword's id
	else:
		id = identifier #to be expanded later, will give identifiers individual ids
		
	return [token, id]
		
	
	
def processLine(line):
	if(len(line) == 0):
		return #if the line is empty, return
	
	global charNumber
	global tokenNum

	charNumber = 0
	tokenNum = 0
	currentChar = line[0]
	token = []
	line_table = []

	while(charNumber < len(line)):
		if(line[charNumber].isalpha() or line[charNumber] == '_'):
			token = processAlphaOr_(line) # Go down the underscore or alpha path
			line_table.append([tokenNum, token])
			tokenNum = tokenNum + 1
		elif(line[charNumber].isdigit()):
			x = 2 #Go down the numeric path
		elif(line[charNumber] == '\"'):
			x = 2 #Go down char path
		elif(line[charNumber] == '+' or line[charNumber] == '-' or line[charNumber] == '*' or
		line[charNumber] == '/' or line[charNumber] == '%'): # need to add <, >, etc
			x = 2 #Go down arithmetic path
		else:
			x = 2	#Get next character
			charNumber += 1
		
	return line_table	
