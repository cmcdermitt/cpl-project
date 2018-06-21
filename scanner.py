#imports
import sys
import csv
from state_machine import processLine
#List of keywords

keywords = dict(zip(['SYMBOL', 'IDENTIFIER', 'HCON', 'FORWARD', 'REFERENCES',
    'MEXTERN', 'FUNCTION', 'MAIN', 'RETURN', 'POINTER', 'ARRAY', 'LB', 'RB','ICON',
    'TYPE', 'STRUCT', 'STRUCTYPE', 'MVOID', 'INTEGER',
    'SHORT', 'REAL', 'FLOAT', 'DOUBLE', 'TBOOL',
    'CHAR', 'TSTRING', 'OF', 'LENGTH', 'ICON',
    'TBYTE', 'SPECIFICATIONS', 'ENUM', 'STRUCT', 'GLOBAL',
    'DECLARATIONS', 'IMPLEMENTATIONS', 'FUNCTION', 'MAIN', 'PARAMETERS',
    'COMMA', 'CONSTANT', 'BEGIN', 'ENDFUN', 'IF',
    'THEN', 'ELSE', 'ENDIF', 'WHILE', 'ENDWHILE',
    'LET', 'REPEAT', 'UNTIL', 'ENDREPEAT', 'DISPLAY'], range(0, 55)))

tokens = []

def main():
  """  print(sys.argv[1])
    linenum = 0
    with open(sys.argv[1]) as infile: #open the file, sys.argv[1] is the first command line argument
        for textline in infile:
            linenum += 1
            line = textline.split() #splits the line into a list of words wherever there's whitespace
            #PROBLEM: Not all tokens will be separated by whitespace. We'll have to do this better later.

            for word in line:
                tokens.append([word, linenum])

    print tokens

    with open('output_scanned.csv', 'w') as outfile: #open output file
        writer = csv.writer(outfile)
        writer.writerows(tokens) #writes each item in tokens to a row of the .csv

print (keywords) """ 
print(processLine("Hellowe232 Cha23r 3222 2.3  3  3   3"))
print(processLine("Hi Cory and Charlie 1234.4568 ad"))
print(processLine("12HI"))
if __name__ == "__main__":
	main()
