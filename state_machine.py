#Move all of this to Scanner.py later 

keywords = dict(zip(['SYMBOL', 'IDENTIFIER', 'HCON', 'FORWARD', 'REFERENCES',
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
symNum = 0

def processAlphaOr_(line):
	global charNumber
	global symNum 
	symbol = ''
	currentChar = line[charNumber]
	while((currentChar.isalpha() or currentChar.isdigit() or currentChar == '_') and charNumber < len(line)):
		currentChar = line[charNumber]
		symbol = symbol + currentChar
		charNumber = charNumber + 1
    
	if(charNumber < len(line)):	
		if(line[charNumber] == '+' or line[charNumber] == '-' or line[charNumber] == '*' or
		line[charNumber] == '/' or line[charNumber] == '%'):
			charNumber = charNumber - 1 #Back up for arithmetic operators
	
	id = keywords.get(symbol)
	if(id == None):
		return [symbol, identifier]
	else:
		return [symbol, id]
		
	
	
def processLine(line):
	if(len(line) == 0):
		return
	global charNumber
	global symNum
	charNumber = 0
	symNum = 0
	currentChar = line[0]
	symbol = []
	line_table = []
	while(charNumber < len(line)):
		print(charNumber)
		if(line[charNumber].isalpha() or line[charNumber] == '_'):
			symbol = processAlphaOr_(line) # Go down the underscore or alpha path
		elif(line[charNumber].isdigit()):
			x = 2 #Go down the numeric path
		elif(line[charNumber] == '\"'):
			x = 2 #Go down char path
		elif(line[charNumber] == '+' or line[charNumber] == '-' or line[charNumber] == '*' or
		line[charNumber] == '/' or line[charNumber] == '%'):
			x = 2 #Go down arithmetic path
		else:
			x = 2	#Get next character
		line_table.append([symNum, symbol])
		symNum = symNum + 1
	return line_table	
