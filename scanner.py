#imports
import sys
import csv
from state_machine import processLine
# List of output tokens and line numbers
tokens = []
# Integer counter for current row
current_row = 0

def main():
	# Attributes list to hold ID, Value, and Type of each keyword in a line
	attributes = []
	# 2D symbol table array to hold attribute data
	# Rows correspond to line number, and columns to line position
	# Initialized as one-dimensional list. Rows added for each attribute list
	symbol_table = []

	#print(sys.argv[1])
	linenum = 0
	with open("sclex1.scl") as infile: #open the file, sys.argv[1] is the first command line argument
		for line in infile:
			linenum += 1
			# ProcessLine returns list of lists containing keyword attributes
			# Structure of single index: [ID, Value, Type]
			# Note: "Type" is represented by the int equivalent of its
			# position in the keywords dictionary
			attributes = processLine(line)
			symbol_table.append(attributes)

			for list in symbol_table:
				if(len(list) == 0):
					symbol_table.remove(list)
		
	for i in range (0, len(attributes)):	
		print(attributes[i])
	with open('output_scanned.csv', 'w') as outfile: #open output file
		writer = csv.writer(outfile)
		writer.writerow (["ID", "Value", "Type", "Line Number", "Line Position"])
		for i in range(0, len(tokens)):
			for j in range(0, len(tokens[i])):
				tokens[i][j].extend([i, j]) #adds line number and position to each entry
			writer.writerows(tokens[i]) #writes each item in tokens to a row of the .csv

""" Test cases
	#print (keywords) 
	print(processLine(" -3222"))
	print(processLine(" Hi Cory and Charlie 1234.4568 ad \"sdsds\" charlie.work \'f\' \'5\'"))
	print(processLine("12HI"))
	print(processLine("0ACDh 023h"))
	print(processLine("\'^\'"))
	print(processLine("ABC\"123\""))"""

if __name__ == "__main__":
	main()