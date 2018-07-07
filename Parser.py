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

#Now each function is expected to start on the first token in it, but we don't assume that it's already checked.

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
		tabs = tabs + '    '
	return tabs

#convenience function returning an error message
#first parameter is what was expected, second is optional location
def error(expected, location = ''):
	if location == '':
		return 'Error: {} expected'.format(expected)
	else:
		return 'Error: {} expected in {}'.format(expected, location)

# Returns the current lex
def nextLex():
	return ['1','2','KEYWORD','MAIN'] # Will be implemented later with scanner

#Will return the current lex
def currentLex():
	return ['3','4','KEYWORD','RETURN']

def prevLex():
		return [] #Will return the last lex


# Prints out the tree using tabs to represent children
def printTree(tree_list, tab):
	if(len(tree_list) == 0):
		return
	print(returnTabs(tab) + tree_list[0]) # Print out the first item in the list; this is the parent node
	if(len(tree_list) == 1):
		return
	for x in range(1, len(tree_list)): # Print out all of its children
		if(isinstance(tree_list[x], str)): # If the child is a string, print it out
			print(returnTabs(tab) + tree_list[x])
		elif(isinstance(tree_list[x], list)): #If the child is a list, indent by 1 and print out that list
			printTree(tree_list[x],tab + 1)
		else:
			print(returnTabs(tab + 1) + str(tree_list[x]))

def recursiveAppend(input, type = ''):
	is_valid = True
	while(is_valid):
		if(len(input) > 0):
			if(isinstance(input[1], list)):
				if(input[1][0] == type or type == ''):
					input = input[1]
				else:
					is_valid = False
			else:
				is_valid = False
		else:
			is_valid = False
	return input

# Starting point for parse tree
# Initially, lex_list is ['Program']
# After appending func_main(), lex_list might be ['Program',[func_main, ['0','0','KEYWORD','FUNCTION'], ['1','1',IDENTIFER, 'MAIN'], [oper_type,['2','2','KEYWORD','RETURN']]]]
# The second pair of braces represents the entirety of func_main
# The third pair in this case, represents the individual lexeme (there could be more in this list)
def program_start():
	lex_list = ['Program']

	scanner.start() #fills symbol table and sets scanner.lex
	lex_list.append(func_main())

	if(scanner.lex[lex_en['value']] == 'GLOBAL'):
		lex_list.append(f_globals()) #called f_globals becasue globals is a function
	#if(scanner.lex[lex_en['value']] == 'IMPLEMENTATIONS'):
		#lex_list.append(implementations())
	else:
		lex_list.append('\tError: Keyword IMPLEMENTATIONS expected')
		scanner.next()
	printTree(lex_list, 0)


# Functions for func_main
def func_main():
	lex_list = ['func_main']
	if(scanner.lex[lex_en['value']] == 'MAIN'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		return lex_list
	elif(scanner.lex[lex_en['value']] == 'FUNCTION'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		if(scanner.lex[lex_en['type']] == 'IDENTIFIER'):
			lex_list.append(tuple(scanner.lex))
			scanner.next()
		else:
			lex_list.append(['\tError: Identifer was expected'])
		if(scanner.lex[lex_en['value']] == 'RETURN'):
			lex_list.append(oper_type())
		else:
			lex_list.append(['\tError: Keyword Return was expected'])
	else:
		lex_list.append(['\tError Main function missing'])
	return lex_list


def oper_type():
	lex_list = ['oper_type']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	if(scanner.lex[lex_en['value']] == 'POINTER'):
		lex_list.append(chk_ptr())
		scanner.next()
	if(scanner.lex[lex_en['value']] == 'ARRAY'):
		lex_list.append(chk_array())
	word = scanner.lex[lex_en['value']]
	if(word == 'TYPE' or word == 'STRUCT' or word == 'IDENTIFIER'):
		lex_list.append(ret_type())
		print (scanner.lex)
	else:
		lex_list.append('\tError: The keywords STRUCT or TYPE or an IDENTIFIER was expected')
	# Not done yet
	return lex_list


def chk_ptr():
	lex_list = ['chk_ptr']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	if(scanner.lex[lex_en['value']] == 'OF'):
		lex_list.append(tuple(scanner.lex))
	else:
		lex_list.append('\tERROR: Keyword OF was expected')
	return lex_list

def chk_array():
	lex_list = ['chk_array']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	if(scanner.lex[lex_en['value']] != 'LB'):
		lex_list.append('\t Error Keyword LB expected')
		return lex_list
	else:
		lex_list.append(array_dim_list())
	return lex_list

# def array_dim_list(): Old but modified since last working
# 	lex_list = ['array_dim_list']
# 	lex_list.append(tuple(scanner.lex))
# 	scanner.next()
# 	if(scanner.lex[lex_en['type']] == 'IDENTIFIER'):
# 		lex_list.append(array_index())
# 		scanner.next()
# 	else:
# 		lex_list.append('\tError: Identifier was expected')
# 	if(scanner.lex[lex_en['value']] == 'RB'):
# 		lex_list.append(tuple(scanner.lex))
# 		scanner.next()
# 	else:
# 		lex_list.append('\tError: Keyword RB was expected')
# 	if(scanner.peek()[lex_en['value']] == 'LB'):
# 		scanner.next()
# 		n_lex = array_dim_list()
# 		x = recursiveAppend(n_lex, 'array_dim_list')
# 		x.insert(1, lex_list)
# 		lex_list = n_lex
# 		#lex_list.insert(1,array_dim_list())
# 	return lex_list

def array_dim_list():
	lex_list = ['array_dim_list']
	while scanner.lex[lex_en['value']] == 'LB': #use while for multiple array_dim_lists instead of recursion
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		if scanner.lex[lex_en['type']] == 'IDENTIFIER' or scanner.lex[lex_en['value']] == 'ICON':
			lex_list.append(array_index())
			if scanner.lex[lex_en['value']] == 'RB':
				lex_list.append(tuple(scanner.lex))
				scanner.next()
			else:
				scanner.next()
				lex_list.append('Error: Keyword RB expected')
		else:
			scanner.next()
			lex_list.append('Error: IDENTIFIER or ICON expected')
	return lex_list



def array_index():
	lex_list = ['array_index']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	return lex_list

def ret_type():
	lex_list = ['ret_type']
	lex_list.append(tuple(scanner.lex))
	if(scanner.lex[lex_en['value']] == 'TYPE'):
		scanner.next()
		type = scanner.lex[lex_en['value']]
		if(type == 'MVOID' or type == 'INTEGER' or type == 'REAL' or type == 'TBOOL'
		 or type == 'CHAR' or type == 'TSTRING'):
			lex_list.append(type_name())
			scanner.next()
			return lex_list
	if(scanner.lex[lex_en['value']] == 'STRUCT' or scanner.lex[lex_en['value']] == 'STRUCTYPE'): #STRUCTTYPE?
		scanner.next()
		if(scanner.lex[lex_en['type']] == 'IDENTIFIER'):
			lex_list.append(tuple(scanner.lex))
			scanner.next()
			return lex_list
		else:
			lex_list.append('\tError: Identifier was expected')
			return lex_list
	return lex_list

def type_name():
	lex_list = ['type_name']
	lex_list.append(tuple(scanner.lex))
	return lex_list

def f_globals():
	lex_list = ['globals']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	if(scanner.lex[lex_en['value']] == 'DECLARATIONS'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('\tError Keyword DECLARATIONS was expected')

	if(scanner.lex[lex_en['value']] == 'CONSTANTS'):
		lex_list.append(const_dec())
	else:
		lex_list.append(error('DECLARATIONS', 'f_globals'))
		return lex_list

	if(scanner.lex[lex_en['value']] == 'VARIABLES'):
	 	lex_list.append(var_dec())
	else:
		lex_list.append(error('VARIABLES', 'f_globals'))
		return lex_list

	if(scanner.lex[lex_en['value']] == 'STRUCT'):
	 	lex_list.append(struct_dec())
	else:
		lex_list.append(error('STRUCT', 'f_globals'))
	return lex_list

def const_dec():
	lex_list = ['const_dec']
	if scanner.lex[lex_en['value']] == 'CONSTANTS':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('Error: Keyword CONSTANTS expected')
		return lex_list
	if(scanner.lex[lex_en['value']] == 'DEFINE'):
		lex_list.append(data_declarations())
	else:
		lex_list.append('\tError Keyword DEFINE expected')
	return lex_list

def var_dec():
	lex_list = ['var_dec']
	if scanner.lex[lex_en['value']] == 'VARIABLES':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('Error: Keyword VARIABLES expected')
		return lex_list
	if(scanner.lex[lex_en['value']] == 'DEFINE'):
		lex_list.append(data_declarations())
	else:
		lex_list.append('\tError Keyword DEFINE expected')
	return lex_list

def struct_dec():
	lex_list = ['struct_dec']
	if scanner.lex[lex_en['value']] == 'STRUCT':	
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('Error: Keyword STRUCT expected in struct_dec')
	if(scanner.lex[lex_en['value']] == 'DEFINE'):
		lex_list.append(data_declarations())
	else:
		lex_list.append('\tError Keyword DEFINE expected')
	return lex_list


def data_declarations():
	lex_list = ['data_declarations']
	if scanner.lex[lex_en['value']] == 'DEFINE': #check validity before starting while loop
		while(scanner.lex[lex_en['value']] == 'DEFINE'):
			lex_list.append(comp_declare())

	else:
		lex_list.append('Error: keyword DEFINE expected in data_declarations')
	return lex_list

def comp_declare():
	lex_list = ['comp_declare']
	if scanner.lex[lex_en['value']] == 'DEFINE':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('Error: keyword DEFINE expected in comp_declare')
	if(scanner.lex[lex_en['type']] == 'IDENTIFIER'):
		lex_list.append(data_declaration())
	else:
		lex_list.append('\tError IDENTIFIER expected')
	return lex_list

def data_declaration():
	lex_list = ['data_declaration']
	if scanner.lex[lex_en['type']] == 'IDENTIFIER':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('DEFINE', 'data_declaration'))

	word = scanner.lex[lex_en['value']]
	if(word == 'ARRAY' or word == 'LB' or word == 'VALUE' or word == 'EQUOP'):
		lex_list.append(parray_dec())
	else:
		lex_list.append(error('ARRAY or LB or VALYE or EQUOP', 'data_declaration'))
	if(scanner.lex[lex_en['value']] == 'OF'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('\tError Keyword OF expected')
	word = scanner.lex[lex_en['value']]
	if(word == 'TUNSIGNED' or word == 'CHAR' or word == 'INTEGER' or
	word == 'MVOID' or word == 'REAL' or word == 'TSTRING' or word == 'TBOOL'):
		lex_list.append(data_type())
		scanner.next()
	else:
		lex_list.append('\tError Type expected')
	return lex_list

def parray_dec():
	lex_list = ['parray_dec']
	if(scanner.lex[lex_en['value']] == 'ARRAY'):
		scanner.next()
		if(scanner.lex[lex_en['value']] == 'LB'):
			lex_list.append(plist_const())
		else:
			lex_list.append('\tError Keyword LB was expected')
		if(scanner.lex[lex_en['value']] == 'VALUE'):
			lex_list.append(popt_array_val())
	else:
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	return lex_list

#def plist_const():
#	lex_list = ['plist_const']
#	lex_list.append(tuple(scanner.lex))
#	scanner.next()
#	if(scanner.lex[lex_en['type']] == 'IDENTIFIER'):
#		lex_list.append(iconst_ident())
#		scanner.next()
#	else:
#		lex_list.append('\tError Identifier was expected')
#	if(scanner.lex[lex_en['value']] == 'RB'):
#		lex_list.append(tuple(scanner.lex))
#		scanner.next()
#	else:
#		lex_list.append('\tError Keyword RB was expected')
#	if(scanner.peek()[lex_en['value']] == 'LB'):
#		scanner.next()
#		n_lex = plist_const()
#		x = recursiveAppend(n_lex, 'plist_const')
#		x.insert(1,lex_list)
#		lex_list = n_lex
#		#lex_list.insert(1,plist_const())
#	return lex_list

def plist_const():
	lex_list = ['plist_const']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	if(scanner.lex[lex_en['type']] == 'IDENTIFIER'):
		lex_list.append(iconst_ident())
		scanner.next()
	else:
		lex_list.append('\tError Identifier was expected')
	if(scanner.lex[lex_en['value']] == 'RB'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('\tError Keyword RB was expected')
	while(scanner.lex[lex_en['value']] == 'LB'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		if (scanner.lex[lex_en['type']] == 'IDENTIFIER'):
			lex_list.append(iconst_ident())
			scanner.next()
		else:
			lex_list.append('\tError Identifier was expected')
		if (scanner.lex[lex_en['value']] == 'RB'):
			lex_list.append(tuple(scanner.lex))
			scanner.next()
		else:
			lex_list.append('\tError Keyword RB was expected')
	return lex_list

def iconst_ident():
	lex_list = ['iconst_ident']
	lex_list.append(tuple(scanner.lex))
	return lex_list

def popt_array_val():
	lex_list = ['popt_array_val']
	lex_list.append(value_eq())
	if(scanner.lex[lex_en['value']] == 'LB'):
		lex_list.append(array_val())
	else:
		lex_list.append(error('LB', 'popt_array_val'))
	return lex_list

def value_eq():
	lex_list = ['value_eq']
	if scanner.lex[lex_en['value']] == 'EQUOP' or scanner.lex[lex_en['value']] == 'VALUE':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('EQUOP or VALUE', 'value_eq'))
	return lex_list

def array_val():
	lex_list = ['array_val']
	lex_list.append(simp_arr_val())
	return lex_list

def simp_arr_val():
	lex_list = ['simp_arr_val']

	if scanner.lex[lex_en['value']] == 'LB':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('LB', 'simp_arr_val'))
	lex_list.append(arg_list())
	if(scanner.lex[lex_en['value']] == 'RB'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append('\tError, RB was expected')
	return lex_list

def arg_list():
	lex_list = ['arg_list']
	valid_types = ['IDENTIFIER', 'STRING', 'LETTER', 'ICON', 'HCON', 'FCON']
	valid_values = ['MINUS', 'NEGATE', 'MTRUE', 'MFALSE', 'LP']
	while (scanner.peek()[lex_en['type']] in valid_types or scanner.peek()[lex_en['value']] in valid_values):
		lex_list.append(expr())
		if(scanner.lex[lex_en['value']] == 'COMMA'):
			lex_list.append(scanner.lex)
			scanner.next()
	return lex_list

def data_type():
	lex_list = ['data_type']
	lex_list.append(tuple(scanner.lex))
	return lex_list

def expr():
	lex_list = ['expr']
	lex_list.append(term())
	if (scanner.lex[lex_en['value']] == 'PLUS' or scanner.lex[lex_en['value']] == 'MINUS'
			or scanner.lex[lex_en['value']] == 'BAND' or scanner.lex[lex_en['value']] == 'BOR'
			or scanner.lex[lex_en['value']] == 'BXOR'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	lex_list.append(term())
	return lex_list

def term():
	lex_list = ['term']
	lex_list.append(punary())

	if (scanner.lex[lex_en['value']] == 'STAR' or scanner.lex[lex_en['value']] == 'DIVOP'
			or scanner.lex[lex_en['value']] == 'MOD' or scanner.lex[lex_en['value']] == 'LSHIFT'
			or scanner.lex[lex_en['value']] == 'RSHIFT'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		lex_list.append(punary)
	return lex_list

def punary():
	lex_list = ['punary']
	if scanner.lex[lex_en['value']] == 'MINUS' or scanner.lex[lex_en['value']] == 'NEGATE':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		lex_list.append(element())
	else:
		lex_list.append(element())
	return lex_list

def element():
	lex_list = ['element']
	valid_types = ['STRING', 'LETTER', 'ICON', 'HCON', 'FCON']
	valid_values = ['MTRUE', 'MFALSE']

	if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	elif scanner.lex[lex_en['type']] == 'IDENTIFIER':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		lex_list.append(popt_ref())
	elif scanner.lex[lex_en['value']] == 'LP':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		lex_list.append(expr())
		if scanner.lex[lex_en['value']] == 'RP':
			lex_list.append(tuple(scanner.lex))
			scanner.next()
		else:
			lex_list.append(error('RP', 'element'))
			return lex_list
	return lex_list

def popt_ref():
	lex_list = ['popt_ref']
	if scanner.lex[lex_en['value']] == 'LB':
		lex_list.append(array_val())
	elif scanner.lex[lex_en['value']] == 'LP':
		lex_list.append(parguments())
	else:
		lex_list.append(error('LP or LB', 'popt_ref'))
		return lex_list
	return lex_list

def parguments():
	lex_list = ['parguments']
	if scanner.lex[lex_en['value']] == 'LP':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('LP', 'parguments'))
		return lex_list
	lex_list.append(arg_list())
	if scanner.lex[lex_en['value']] == 'RP':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('RP', 'parguments'))
		return lex_list
	




	

def struct_enum():
	lex_list = ['struct_enum']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	if scanner.lex[lex_en['value']] == 'STRUCT' or scanner.lex[lex_en['value']] == 'ENUM':
		lex_list.append(tuple(scanner.lex))
	else:	
		lex_list.append('Error: Keyword STRUCT or ENUM expected')
	return lex_list 

if __name__ == '__main__':
	program_start()