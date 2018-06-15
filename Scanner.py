#imports
import getopt, sys

#List of keywords

keywords = dict(zip(range (101, 155), ['SYMBOL', 'IDENTIFIER', 'HCON', 'FORWARD', 'REFERENCES',
    'MEXTERN', 'FUNCTION', 'MAIN', 'RETURN', 'POINTER', 'ARRAY', 'LB', 'RB','ICON',
    'TYPE', 'STRUCT', 'STRUCTYPE', 'MVOID', 'INTEGER',
    'SHORT', 'REAL', 'FLOAT', 'DOUBLE', 'TBOOL',
    'CHAR', 'TSTRING', 'OF', 'LENGTH', 'ICON',
    'TBYTE', 'SPECIFICATIONS', 'ENUM', 'STRUCT', 'GLOBAL',
    'DECLARATIONS', 'IMPLEMENTATIONS', 'FUNCTION', 'MAIN', 'PARAMETERS',
    'COMMA', 'CONSTANT', 'BEGIN', 'ENDFUN', 'IF',
    'THEN', 'ELSE', 'ENDIF', 'WHILE', 'ENDWHILE',
    'LET', 'REPEAT', 'UNTIL', 'ENDREPEAT', 'DISPLAY']))

	
def main(argv):
	print(sys.argv[1])
	
print (keywords) 
if __name__ == "__main__":
	main(sys.argv[1])