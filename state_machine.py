

charNumber = 0

def processAlphaOr_(line):
	name = ''
	currentChar = line[charNumber]
	while(currentChar.isalpha || currentChar.isDigit || currentChar == '_'):
		symbol.append(currentChar)
       	charNumber = charNumber + 1
       	currentChar = line[charNumber]
       	
	if(line[charCount] == '+' || line[charCount] == '-' || line[charCount] == '*' ||
		line[charCount] == '/' || line[charCount] == '%'):
			charNumber = charNumber - 1 #Back up for arithmetic operators
			
	
	


def processLine(line):
	if(len(line) == 0):
		return
	charNumber = 0
	symNumber = 0
	currentChar = line[0]
	symbol = []
	line_table = [][]
	while(charCount <= len(line)):
		if(line[charCount].isalpha() || line[charCount] == '_'):
			x = 2 # Go down the underscore or alpha path
		else if(line[charCount].isdigit()):
			x = 2 #Go down the numeric path
		else if(line[charCount] == '\"'):
			x = 2 #Go down char path
		else if(line[charCount] == '+' || line[charCount] == '-' || line[charCount] == '*' ||
		line[charCount] == '/' || line[charCount] == '%'):
			x = 2 #Go down arithmetic path
		else:
			#Get next character
		line_table.append(symNumber)
		line_table[charNumber].append(symbol)
		symNumber = symNumber + 1
		charCount = charCount + 1
		
