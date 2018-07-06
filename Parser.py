from enum import Enum
from scanner import Scanner
import sys

'''
Parser.py
The parser uses the recursive-descent method of parsing,
where each left hand definition is represented as a function.
The root of the parse tree is the function program.
Each function calls the functions of the right hand components after checking if it is possible to use those components by looking ahead
The original caller has a list called lexeme_list. lexeme_list is appended the return value of each function called. Each return value is a list.
Each of those functions in turn calls other subfunctions that will append the return value of the called function to their own lexeme_list.
However, there are two cases to consider.
If there are multiple right hand definitions, only one will be correct. Sometimes, the wrong function will be chosen first and as a result nothing will be returned.
If this is the case, then the integer current_lex needs to be reverted to its value before calling the function.
The document has errors in it. If all right hand definitions are exhausted and none of them work (at a certain level), then an error message is created at some level
In this case, the c_lex value must not be reverted, because parsing must recover and continue.
ISSUE: Where do we decide to put the error. Theoretically, it could be at the root of the tree.
POSSIBLE SOLUTION: Certain definitions are considered "choke points for errors" like action_def. RESOLVED
If one action_def in a pactions is malformed, the pactions should continue to process more action_defs.
lexeme_list = a recursive list lexemes [lexeme[[sublexeme1[sub sub lexeme]] ... [sublexeme[sublexeme]]]]
ISSUE: When do we decide to add more lexemes to the initial pool of lexemes.
POSSIBLE SOLUTION: We call the scanner and get all of the lexemes at once. We then append Nothing to the end to signify the last lexeme has been read. RESOLVED: Addded as needed with look back functions
'''

'''
Sorry for globals, but every function needs these, (unless we pass object?):
	global c_lex
	global t_lex
'''

'''
NOTES:
Every time you go into a function, the first lexeme
Every time you add a lexeme, put it in a tuple.
'''


#lex_en = {'ID' : 0, 'Pos' : 1, 'type' : 2, 'value': 3}
lex_en = {'value' : 0, 'type' : 1}
scanner = Scanner(sys.argv[1])
c_lex = []

# Returns number of tabs
def returnTabs(tabNum):
	tabs = ''
	for i in range(tabNum):
		tabs = tabs + '\t'
	return tabs

# Returns the current lex
def nextLex():
	return ['1','2','KEYWORD','MAIN'] # Will be implemented later with scanner

#Will return the current lex
def currentLex():
	return ['3','4','KEYWORD','RETURN']

def prevLex():
		return [] #Will return the last lex


# Prints out the tree using tabs to represent children
#
def printTree(tree_list, tab):
	if(len(tree_list) == 0):
		return
	print(returnTabs(tab) + tree_list[0]) # Print out the first item in the list; this is the parent node
	if(len(tree_list) == 1):
		return
	for x in range(1,	len(tree_list)): # Print out all of its children
		if(isinstance(tree_list[x], str)): # If the child is a string, print it out
			print(returnTabs(tab) + tree_list[x])
		elif(isinstance(tree_list[x], list)): #If the child is a list, indent by 1 and print out that list
			printTree(tree_list[x],tab + 1)
		else:
			print(returnTabs(tab + 1) + str(tree_list[x]))

# Starting point for parse tree
# Initially, lex_list is ['Program']
# After appending func_main(), lex_list might be ['Program',[func_main, ['0','0','KEYWORD','FUNCTION'], ['1','1',IDENTIFER, 'MAIN'], [oper_type,['2','2','KEYWORD','RETURN']]]]
# The second pair of braces represents the entirety of func_main
# The third pair in this case, represents the individual lexeme (there could be more in this list)
def program_start():
	lex_list = ['Program']
	lex_list.append(func_main())
	lex = scanner.getNextToken()
	printTree(lex_list, 0)
	if(lex[lex_en['value']] == 'GLOBAL'):
		lex_list.append(f_globals()) #called f_globals becasue globals is a fucntion
		lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'IMPLEMENTATIONS'):
		lex_list.append(implementations())
	else:
		lex_list.append('\tError: Keyword IMPLEMENTATIONS expected')


# Functions for func_main
def func_main():
	lex_list = ['func_main']
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'MAIN'):
		lex_list.append(tuple(lex))
		return lex_list
	elif(lex[lex_en['value']] == 'FUNCTION'):
		lex_list.append(tuple(lex))
		lex = scanner.getNextToken()
		if(lex[lex_en['type']] == 'IDENTIFIER'):
			lex_list.append(tuple(lex))
			lex = scanner.getNextToken()
		else:
			lex_list.append(['\tError: Identifer was expected'])
		if(lex[lex_en['value']] == 'RETURN'):
			lex_list.append(oper_type())
		else:
			lex_list.append(['\tError: Keyword Return was expected'])
	else:
		lex_list.append(['\tError Main function missing'])
	return lex_list


def oper_type():
	lex_list = ['oper_type']
	lex_list.append(tuple(scanner.getCurrentToken()))
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'POINTER'):
		lex_list.append(chk_ptr())
		lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'ARRAY'):
		lex_list.append(chk_array())
		lex = scanner.getNextToken()
	word = lex[lex_en['value']]
	if(word == 'TYPE' or word == 'STRUCT' or word == 'IDENTIFIER'):
		lex_list.append(ret_type())
	else:
		lex_list.append('\tError: The keywords STRUCT or TYPE or an IDENTIFIER was expected')
	# Not done yet
	return lex_list

def chk_ptr():
	lex_list = ['chk_ptr']
	lex_list.append(tuple(scanner.getCurrentToken()))
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'OF'):
		lex_list.append(tuple(lex))
	else:
		lex_list.append('\tERROR: Keyword OF was expected')
	return lex_list

def chk_array():
	lex_list = ['chk_array']
	lex_list.append(tuple(scanner.getCurrentToken()))
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] != 'LB'):
		lex_list.append('\t Error Keyword LB expected')
		return lex_list
	lex_list.append(array_dim_list())
	return lex_list

def array_dim_list():
	lex_list = ['array_dim_list']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	if(lex[lex_en['type']] == 'IDENTIFIER'):
		lex_list.append(array_index())
		lex = scanner.getNextToken()
	else:
		lex_list.append('\tError: Identifier was expected')
	if(lex[lex_en['value']] == 'RB'):
		lex_list.append(tuple(lex))
	else:
		lex_list.append('\tError: Keyword RB was expected')
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'LB'):
		lex_list.insert(1,array_dim_list())
	else:
		scanner.rewindCurrentToken()
	return lex_list

def array_index():
	lex_list = ['array_index']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	return lex_list

def ret_type():
	lex_list = ['ret_type']
	lex = scanner.getCurrentToken()
	word = lex[lex_en['value']]
	lex_list.append(tuple(lex))
	if(word == 'TYPE'):
		type = lex[lex_en['type']]
		if(
			type == 'MVOID' or
			type == 'INTEGER' or
			type == 'REAL' or
			type == 'TBOOL' or
			type == 'CHAR' or
			type == 'TSTRING'
		):
			lex_list.append(type_name())
			return lex_list
	if(lex[lex_en['value']] == 'STRUCT' or lex[lex_en['value']] == 'STRUCTYPE'): #STRUCTTYPE?
		lex = scanner.getNextToken()
		if(lex[lex_en['type']] == 'IDENTIFIER'):
			lex_list.append(tuple(lex))
			return lex_list
		else:
			lex_list.append('\tError: Identifier was expected')
			return lex_list

	return lex_list

def type_name():
	lex_list = []
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	return lex_list
'''	if(lex[lex_en['value']] == 'TSTRING'):
		lex_list.append(lex)
		lex = scanner.getNextToken()
		if(lex[lex_en['value']] == 'OF'):  Is TSTRING relevant? ICON is an
		unknown keyword'''

def struct_enum():
	lex_list = ['struct_enum']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	if lex[lex_en['value']] 	== 'STRUCT' or lex[lex_en['value']] == 'ENUM':
		lex_list.append(tuple(lex))
	else:	
		lex_list.append('Error: Keyword STRUCT or ENUM expected')
	return lex_list 

def specifications():
	lex_list = ['specifications']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	if (
		lex[lex_en['value']] == 'ENUM' or
		lex[lex_en['value']] == 'STRUCT' or
		lex[lex_en['value']] == 'DESCRIPTION'
	):
		lex_list.append(spec_list())
	else:
		lex_list.append('Error: Keyword ENUM, STRUCT, or DESCRIPTION expected')'' \
	return lex_list

def spec_list():
	lex_list = ['spec_list']
	lex = scanner.getCurrentToken()
	lex_list.append(spec_def())
	lex = scanner.getNextToken()
	if (lex[lex_en['value']] == 'ENUM' or lex[lex_en['value']] == 'STRUCT' or
	    lex[lex_en['value']] == 'DESCRIPTION'):
		lex_list.append(spec_def())
	else:
		return lex_list

def spec_def():
	lex_list = ['spec_def']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	return lex_list

def f_globals():
	lex_list = ['globals']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'GLOBAL'):
		lex_list.append(tuple(lex))
		lex = scanner.getNextToken()
	else:
		lex_list.append('Error Keyword GLOBAL was expected')
	if(lex[lex_en['value']] == 'DECLARATIONS'):
		lex_list.append(tuple(lex))
		lex = scanner.getNextToken()
	else:
		lex_list.append('Error Keyword DECLARATIONS was expected')
	if(lex[lex_en['value']] == 'CONSTANTS'):
		lex_list.append(const_dec())
		lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'VARIABLES'):
		lex_list.append(var_dec())
		lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'STRUCT'):
		lex_list.append(struct_dec())
		lex = scanner.getNextToken()

def const_dec():
	lex_list = ['const_dec']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'DEFINE'):
		lex_list.append(data_declarations())
	return lex_list

def var_dec():
	lex_list = ['var_dec']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'DEFINE'):
		lex_list.append(data_declarations())
	return lex_list

def struct_dec():
	lex_list = ['struct_dec']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	if(lex[lex_en['value']] == 'DEFINE'):
		lex_list.append(data_declarations())
	return lex_list

def data_declarations(): #unfinished
	lex_list = ['data_declarations']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	lex = scanner.getNextToken()
	value = lex[lex_en['value']]
	if (
		value == 'ARRAY' or
		value == 'LB' or
		value == 'VALUE' or
		value == 'EQUOP'
	):
		lex_list.append(parray_dec())
	else:
		return lex_list.append('Error: Keyword ARRAY, LB, VALUE, or EQUOP expected')
	lex = scanner.getNextToken()
	if lex[lex_en['value']] == 'OF':
		lex_list.append(tuple(lex))
	else:
		return lex_list.append('ERROR: Keyword OF expected')
	lex = scanner.getNextToken()
	value = lex[lex_en['value']]
	if (
		value == 'TUNSIGNED' or
		value == 'CHAR' or
		value == 'INTEGER' or
		value == 'MVOID' or
		value == 'DOUBLE' or
		value == 'LONG' or
		value == 'SHORT' or
		value == 'FLOAT' or
		value == 'REAL' or
		value == 'TSTRING' or
		value == 'TBOOL' or
		value == 'TBYTE'
	):
		lex_list.append(data_type())
	else:
		return lex_list.append('Error: Data_type keyword expected')
	return lex_list

def parray_dec():
	lex_list = ['parray_dec']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	if lex[lex_end['value']] == 'ARRAY':
		lex = scanner.getNextToken()
		if lex[lex_en['value']] == 'LB':
			lex_list.append(tuple(lex))
			lex = scanner.getNextToken()
			if lex[lex_en['value']] == 'ICON' or lex[lex_en['value']] == 'IDENTIFIER':
				lex_list.append(plist_const())
			elif (
					lex[lex_en['value']] == 'IDENTIFIER' or
					lex[lex_en['value']] == 'STRING' or
					lex[lex_en['value']] == 'LETTER' or
					lex[lex_en['value']] == 'ICON' or
					lex[lex_en['value']] == 'HCON' or
					lex[lex_en['value']] == 'FCON' or
					lex[lex_en['value']] == 'MTRUE' or
					lex[lex_en['value']] == 'MFALSE' or
					lex[lex_en['value']] == 'LP' or
					lex[lex_en['value']] == 'MINUS' or
					lex[lex_en['value']] == 'NEGATE'
			):
				lex_list.append(expr())
		else:
			lex_list.append('Error: Keyword LB expected')


def data_type():
	lex_list = ['data_type']
	lex = scanner.getCurrentToken()
	lex_list.append(tuple(lex))
	return lex_list




if __name__ == '__main__':
	program_start()
