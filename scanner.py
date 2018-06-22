#imports
import sys
import csv
from state_machine import processLine
#List of keywords

# OUT OF DATE - use state_machine keywords list
# keywords = dict(zip(['SYMBOL', 'IDENTIFIER', 'HCON', 'FORWARD', 'REFERENCES',
# 	'MEXTERN', 'FUNCTION', 'MAIN', 'RETURN', 'POINTER', 'ARRAY', 'LB', 'RB','ICON',
# 	'TYPE', 'STRUCT', 'STRUCTYPE', 'MVOID', 'INTEGER',
# 	'SHORT', 'REAL', 'FLOAT', 'DOUBLE', 'TBOOL',
# 	'CHAR', 'TSTRING', 'OF', 'LENGTH', 'ICON',
# 	'TBYTE', 'SPECIFICATIONS', 'ENUM', 'STRUCT', 'GLOBAL',
# 	'DECLARATIONS', 'IMPLEMENTATIONS', 'FUNCTION', 'MAIN', 'PARAMETERS',
# 	'COMMA', 'CONSTANT', 'BEGIN', 'ENDFUN', 'IF',
# 	'THEN', 'ELSE', 'ENDIF', 'WHILE', 'ENDWHILE',
# 	'LET', 'REPEAT', 'UNTIL', 'ENDREPEAT', 'DISPLAY'], range(0, 55)))

# List of output tokens and line numbers
tokens = []
# 2D symbol table array to hold attribute data
# Rows correspond to line number, and columns to line position
symbol_table = [0][0]
# Attributes list to hold ID, Value, and Type of each keyword in a line
attributes = []
# Integer counter for current row
current_row = 0

def main():
	
	"""
	print(sys.argv[1])
	linenum = 0
	with open(sys.argv[1]) as infile: #open the file, sys.argv[1] is the first command line argument
		for i, line in enumerate(infile):
			linenum += 1
			#line = textline.split() #splits the line into a list of words wherever there's whitespace
			#PROBLEM: Not all tokens will be separated by whitespace. We'll have to do this better later.
			# ProcessLine returns list of lists containing keyword attributes
			# Structure of single index: [ID, Value, Type]
			# Note: "Type" is represented by the int equivalent of its
			# position in the keywords dictionary
			attributes = processLine(line)

			for sub_list in attributes:
				if len(sub_list) > 1:
					# position = attributes.index(sub_list), 0, len(attributes))
					position = i
					symbol_table[current_row][position] = sub_list

			currentRow = currentRow + 1

			for word in line:
				tokens.append([word, linenum])

	with open('output_scanned.csv', 'w') as outfile: #open output file
		writer = csv.writer(outfile)
		writer.writerow (["ID", "Value", "Type", "Line Number", "Line Position"])
		for i in range(0, len(tokens)):
			for j in range(0, len(tokens[i])):
				tokens[i][j].extend([i, j]) #adds line number and position to each entry
			writer.writerows(tokens[i]) #writes each item in tokens to a row of the .csv"""

	#print (keywords) 
	print(processLine(" -3222"))
	print(processLine(" Hi Cory and Charlie 1234.4568 ad \"sdsds\" charlie.work \'f\' \'5\'"))
	print(processLine("12HI"))
	print(processLine("0ACDh 023h"))
	print(processLine("\'^\'"))

if __name__ == "__main__":
	main()