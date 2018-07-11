# Authors: Charlie McDermitt
#          Eric Schneider
#          Corey Harris
# Class:   CS4308 - W01
#          Concepts of Programming Languages
# Title:   Final Project - Second Deliverable
# Date:    09 July 2018

from enum import Enum
from scanner import Scanner
import sys

# The parser uses the recursive-descent method of parsing, where each left hand definition is represented as a function.
# The root of the parse tree is the function program.
# Each function calls the functions of the right hand components after checking if it is
# possible to use those components by looking ahead.
# The original caller has a list called lex_list. lex_list is appended
# the return value of each function called. Each return value is a list.
# Each of those functions in turn calls other subfunctions that will append
# the return value of the called function to their own lex_list.
# However, if there are multiple right hand definitions, only one will be correct, so the correct function must be chosen before we enter it.
# If the parser encounters an error, it appends an error message instead of a list.

lex_en = {'value' : 0, 'type' : 1, 'line_num' : 2}
scanner = Scanner(sys.argv[1])

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
		return '\tError: {} expected'.format(expected)
	else:
		return '\tError: {} expected in {}'.format(expected, location)

# Prints out the tree using tabs to represent children
def printTree(tree_list, tab, out_string = ''):
	if(len(tree_list) == 0):
		return
	if len(sys.argv) > 2: #if there's an output file name
		out_string = out_string + returnTabs(tab) + tree_list[0] + '\n' # Print out the first item in the list; this is the parent node
		if(len(tree_list) == 1):
			return
		for x in range(1, len(tree_list)): # Print out all of its children
			if(isinstance(tree_list[x], str)): # If the child is a string, print it out
				out_string = out_string + returnTabs(tab) + tree_list[x] + '\n'
			elif(isinstance(tree_list[x], list)): #If the child is a list, indent by 1 and print out that list
				out_string = printTree(tree_list[x], tab + 1, out_string)
			else:
				out_string = out_string + returnTabs(tab + 1) + str(tree_list[x]) + '\n'
		with open(sys.argv[2], 'w') as outfile:
			outfile.write(out_string)
	else: #if no output file name is provided, print the output
		print(returnTabs(tab) + tree_list[0]) # Print out the first item in the list; this is the parent node
		if(len(tree_list) == 1):
			return
		for x in range(1, len(tree_list)): # Print out all of its children
			if(isinstance(tree_list[x], str)): # If the child is a string, print it out
				print(returnTabs(tab) + tree_list[x])
			elif(isinstance(tree_list[x], list)): #If the child is a list, indent by 1 and print out that list
				printTree(tree_list[x], tab + 1)
			else:
				print(returnTabs(tab + 1) + str(tree_list[x]))
	return out_string


def printCleanTree(tree_list, tab, printTree = False, out_string = ''):
	if(len(tree_list) == 0):
		return out_string
	out_string +=  returnTabs(tab) + ( ('Enter <' + tree_list[0] + '>\n'))
	if(len(tree_list) == 1):
		return out_string
	for x in range(1, len(tree_list)):
		if(isinstance(tree_list[x], str)):
			out_string +=  returnTabs(tab) + tree_list[x] + '\n'
		elif(isinstance(tree_list[x], list)):
			out_string = printCleanTree(tree_list[x],tab + 1, False, out_string)
		else:
			out_string +=  returnTabs(tab) + ('Type is ' + str(tree_list[x][lex_en['type']]) + ' Value is ' + str(tree_list[x][lex_en['value']]) + ' at line ' + str(tree_list[x][lex_en['line_num']]) + '\n')
	out_string += returnTabs(tab) + (('Exit <' + tree_list[0] + '>\n'))
	return out_string



# Starting point for parse tree
# Each function following this checks the unique case that defines its particular grammar as defined by the document
# The general structure instantiates a new instance of lex_list, and sets its initial value to the name of the function
# This creates an easy to follow hierarchy and flow of function calls that can be read and debugged via the output
# The function then retrieves each subsequent lexeme from the symbol table, checks its validity, and adds it to lex_list
# Once the last lexeme has been appended the lex_list, it is returned and appended to the instance of the calling method
# If the function encounters an error, it appends an error message and skips over that lexeme.
# This method of error checking allows to catch each individual error without it crashing the entire system.
def program_start():
	lex_list = ['Program']
	scanner.start()
	lex_list.append(func_main())

	if(scanner.lex[lex_en['value']] == 'GLOBAL'):
		lex_list.append(f_globals()) #called f_globals becasue globals is a function

	lex_list.append(implement())
	print(printCleanTree(lex_list,0, True))

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

def struct_enum():
	lex_list = ['struct_enum']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	if scanner.lex[lex_en['value']] == 'STRUCT' or scanner.lex[lex_en['value']] == 'ENUM':
		lex_list.append(tuple(scanner.lex))
	else:
		lex_list.append('Error: Keyword STRUCT or ENUM expected')
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

	if(scanner.lex[lex_en['value']] == 'VARIABLES'):
	 	lex_list.append(var_dec())
	else:
		lex_list.append(error('VARIABLES', 'f_globals'))
		return lex_list

	if(scanner.lex[lex_en['value']] == 'STRUCT'):
	 	lex_list.append(struct_dec())
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
		lex_list.append(error('IDENTIFIER', 'data_declaration'))

	word = scanner.lex[lex_en['value']]
	if(word == 'ARRAY' or word == 'LB' or word == 'VALUE' or word == 'EQUOP'):
		lex_list.append(parray_dec())

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
	valid_values = ['BAND','BOR', 'BXOR', 'STAR', 'DIVOP', 'MOD', 'LSHIFT', 'RSHIFT' 'PLUS', 'MINUS', 'NEGATE', 'MTRUE', 'MFALSE', 'LP']
	while (scanner.peek()[lex_en['type']] in valid_types or scanner.peek()[lex_en['value']] in valid_values):
		lex_list.append(expr())
		if(scanner.lex[lex_en['value']] == 'COMMA'):
			lex_list.append(scanner.lex)
			scanner.next()
		else:
			return lex_list
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
		if scanner.lex[lex_en['value']] == 'LB' or scanner.lex[lex_en['value']] == 'LB':
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
	else:
		lex_list.append(error('IDENTIFIER or LP or TYPE or MTRUE or MFALSE', 'element'))

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

def parguments():
	lex_list = ['parguments']
	if scanner.lex[lex_en['value']] == 'LP':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('LP', 'parguments'))
	lex_list.append(arg_list())
	if scanner.lex[lex_en['value']] == 'RP':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('RP', 'parguments'))
	return lex_list

def implement():
	lex_list = ['implement']
	if scanner.lex[lex_en['value']] == 'IMPLEMENTATIONS':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('IMPLEMENTATIONS', 'implement'))
	if scanner.lex[lex_en['value']] == 'MAIN':
		lex_list.append(main_head())
	lex_list.append(funct_list())
	return lex_list

def main_head():
	lex_list = ['main_head']
	if scanner.lex[lex_en['value']] == 'MAIN':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('MAIN', 'main_head'))
	if scanner.lex[lex_en['value']] == 'DESCRIPTION':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('DESCRIPTION','main_head'))
	if scanner.lex[lex_en['value']] == 'PARAMETERS':
		lex_list.append(parameters())
	return lex_list

def parameters():
	lex_list = ['parameters']
	lex_list.append(tuple(scanner.lex))
	scanner.next()
	lex_list.append(param_def())
	while scanner.lex[lex_en['value']] == 'COMMA':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		lex_list.append(param_def())
	return lex_list

def param_def():
	lex_list = ['param_def']
	lex_list.append(data_declaration())
	return lex_list

def funct_list():
	lex_list = ['funct_list']
	lex_list.append(funct_body())
	while scanner.lex[lex_en['value']] == 'FUNCTION':
		lex_list.append(funct_body())
	return lex_list

def funct_body():
	lex_list = ['funct_body']
	if scanner.lex[lex_en['value']] == 'FUNCTION':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('FUNCTION', 'funct_body'))
	#lex_list.append(phead_fun()) <- What is this
	lex_list.append(pother_oper_def())
	return lex_list

def pother_oper_def():
	lex_list = ['pother_oper_def']
	lex_list.append(pother_oper())
	if scanner.lex[lex_en['value']] == 'IS':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('IS', 'pother_oper_def'))
	lex_list.append(const_var_struct())
	if(scanner.lex[lex_en['value']] == 'PRECONDITION'):
		lex_list.append(precond())
	if scanner.lex[lex_en['value']] == 'BEGIN':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('BEGIN', 'pother_oper_def'))
	lex_list.append(pactions())
	if scanner.lex[lex_en['value']] == 'ENDFUN':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('ENDFUN', 'pother_oper_def'))
	if scanner.lex[lex_en['type']] == 'IDENTIFIER':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('IDENTIFIER', 'pother_oper_def'))
	return lex_list

def pother_oper():
	lex_list = ['pother_oper']
	if scanner.lex[lex_en['type']] == 'IDENTIFIER':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('IDENTIFIER','pother_oper'))
	if scanner.lex[lex_en['value']] == 'DESCRIPTION':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('DESCRIPTION', 'pother_oper'))
	if scanner.lex[lex_en['value']] == 'RETURN':
		lex_list.append(oper_type())
	if scanner.lex[lex_en['value']] == 'PARAMETERS':
		lex_list.append(parameters())
	return lex_list

def const_var_struct():
	lex_list = ['const_var_struct']

	if(scanner.lex[lex_en['value']] == 'CONSTANTS'):
		lex_list.append(const_dec())

	if(scanner.lex[lex_en['value']] == 'VARIABLES'):
	 	lex_list.append(var_dec())
	else:
		lex_list.append(error('VARIABLES', 'const_var_struct'))
		return lex_list

	if(scanner.lex[lex_en['value']] == 'STRUCT'):
	 	lex_list.append(struct_dec())

	return lex_list

def precond():
	lex_list = ['PRECONDITION']
	if scanner.lex[lex_en['value']] == 'PRECONDITION':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('PRECONDITION', 'precond'))
	lex_list.append(pcondition())
	return lex_list

def pcondition():
	lex_list = ['pcondition']
	lex_list.append(pcond1())
	word = scanner.lex[lex_en['value']]
	if word == 'OR' or word == 'AND':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		lex_list.append(pcond1())
	return lex_list

def pcond1():
	lex_list = ['pcond1']
	if scanner.lex[lex_en['value']] == 'NOT':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	lex_list.append(pcond2())
	return lex_list

def pcond2():
	lex_list = ['pcond2']
	# For LP pcondition RP case
	if scanner.lex[lex_en['value']] == 'LP':
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		lex_list.append(pcondition())
		if scanner.lex[lex_en['value']] == 'RP':
			lex_list.append(tuple(scanner.lex))
			scanner.next()
		else:
			lex_list.append(error('RP', 'pcond2'))
		return lex_list

	valid_types = ['STRING', 'LETTER', 'ICON', 'HCON', 'FCON', 'IDENTIFIER']
	valid_values = ['MTRUE', 'MFALSE']


	# For other cases
	if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
		word = scanner.peek()[lex_en['value']]
		if(word == 'PLUS' or word == 'MINUS' or word == 'BAND' or word == 'BOR'
		or word == 'BXOR' or word == 'STAR' or word == 'DIVOP' or
		word == 'MOD' or word == 'LSHIFT' or word == 'RSHIFT'):
			lex_list.append(expr())
			if scanner.lex[lex_en['value']] == 'RELOP' or scanner.lex[lex_en['value']] == 'EQUOP':
				lex_list.append(tuple(scanner.lex))
				scanner.next()
			elif scanner.lex[lex_en['value']] == 'NOT':
				lex_list.append(opt_not())
				lex_list.append(true_false())
				return lex_list
			elif scanner.lex[lex_en['value']] == 'MTRUE' or scanner.lex[lex_en['type']] == 'MFALSE':
				lex_list.append(true_false())
				return lex_list
			else:
				lex_list.append(eq_v())
			lex_list.append(expr())
			return lex_list
		else:
			lex_list.append(element())
	return lex_list

def opt_not():
	lex_list = ['opt_not']
	if(scanner.lex[lex_en['value']] == 'NOT'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('NOT', 'opt_not'))
	return lex_list

def true_false():
	lex_list = ['true_false']
	if(scanner.lex[lex_en['value']] == 'MTRUE' or scanner.lex[lex_en['value']] == 'MFALSE'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
	else:
		lex_list.append(error('MTrue or MFalse', 'true_false'))
	return lex_list

def eq_v():
	lex_list = ['eq_v']
	if(scanner.lex[lex_en['value']] == 'EQUALS'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		return lex_list
	elif(scanner.lex[lex_en['value']] == 'GREATER' or scanner.lex[lex_en['value']] == 'LESS'):
		lex_list.append(tuple(scanner.lex))
		scanner.next()
		if(scanner.lex[lex_en['value']] == 'THAN'):
			lex_list.append(tuple(scanner.lex))
			scanner.next()
			return lex_list
		elif scanner.lex[lex_en['value']] == 'OR':
			lex_list.append(tuple(scanner.lex))
			scanner.next()
			if scanner.lex[lex_en['value']] == 'EQUAL':
				lex_list.append(tuple(scanner.lex))
				scanner.next()
			else:
				lex_list.append(error('EQUAL', 'eq_v'))
		else:
			lex_list.append('\tError Keywords GREATER or LESS were expected')
	else:
		lex_list.append('\tError Keywords EQUALS or GREATER were expected')
	return lex_list


def pactions():
    lex_list = ['pactions']
    valid_values = ['SET', 'READ', 'INPUT', 'DISPLAY', 'DISPLAYN', 'MCLOSE', 'MOPEN', 'MFILE',
                    'INCREMENT', 'DECREMENT', 'RETURN', 'CALL', 'IF', 'FOR', 'REPEAT',
                    'WHILE', 'CASE', 'MBREAK', 'MEXIT','POSTCONDITION']
    times = 0
    while scanner.lex[lex_en['value']] in valid_values:
        lex_list.append(action_def())
        times += 1
    if times == 0:
        lex_list.append(error('action_def keyword', 'paction'))
    return lex_list

def action_def():
    lex_list = ['action_def']
    # Valid types and values for following the expr() path
    valid_types = ['IDENTIFIER', 'STRING', 'LETTER', 'ICON', 'HCON', 'FCON']
    valid_values = ['MINUS', 'NEGATE', 'MTRUE', 'MFALSE', 'LP']
    # Add current lexeme to lex_list
    lex_list.append(tuple(scanner.lex))
    # Determine path of execution for action_def group
    # Following 'SET' path
    if scanner.lex[lex_en['value']] == 'SET':
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
            lex_list.append(name_ref())
        else:
            lex_list.append(error('IDENTIFIER', 'action_def'))
        if scanner.lex[lex_en['value']] == 'EQUOP':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('EQUOP', 'action_def'))
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            lex_list.append(expr())
        else:
            lex_list.append(error('expr keyword', 'action_def'))
    # Following 'READ' path
    elif scanner.lex[lex_en['value']] == 'READ':
        scanner.next()
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            lex_list.append(pvar_value_list())
        else:
            lex_list.append(error('expr keyword', 'action_def'))
    # Following 'INPUT' path
    elif scanner.lex[lex_en['value']] == 'INPUT':
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
            lex_list.append(name_ref())
        else:
            lex_list.append(error('IDENTIFIER', 'action_def'))
    # Following 'DISPLAY' or 'DISPLAYN' path
    elif (scanner.lex[lex_en['value']] == 'DISPLAY' or
            scanner.lex[lex_en['value']] == 'DISPLAYN'):
        scanner.next()
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            lex_list.append(pvar_value_list())
        else:
            lex_list.append(error('expr keyword', 'action_def'))
    # Following 'MCLOSE' path
    elif scanner.lex[lex_en['value']] == 'MCLOSE':
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('IDENTIFIER', 'action_def'))
    # Following 'MOPEN' path
    elif scanner.lex[lex_en['value']] == 'MOPEN':
        scanner.next()
        if (scanner.lex[lex_en['value']] == 'INPUT' or
                scanner.lex[lex_en['value']] == 'OUTPUT'):
            lex_list.append(in_out())
        else:
            lex_list.append(error('INPUT or OUTPUT', 'action_def'))
    # Following 'MFILE' path
    elif scanner.lex[lex_en['value']] == 'MFILE':
        scanner.next()
        if (scanner.lex[lex_en['value']] == 'READ' or
                scanner.lex[lex_en['value']] == 'WRITE'):
                lex_list.append(read_write())
        else:
            lex_list.append(error('READ or WRITE', 'action_def'))
    # Following 'INCREMENT' or 'DECREMENT' path
    elif (scanner.lex[lex_en['value']] == 'INCREMENT' or
            scanner.lex[lex_en['value']] == 'DECREMENT'):
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
            lex_list.append(name_ref())
        else:
            lex_list.append(error('IDENTIFIER', 'action_def'))
    # Following 'RETURN' path
    elif scanner.lex[lex_en['value']] == 'RETURN':
        scanner.next()
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            lex_list.append(expr())
        else:
            lex_list.append(error('expr keyword', 'action_def'))
    # Following 'CALL' path
    elif scanner.lex[lex_en['value']] == 'CALL':
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
            lex_list.append(name_ref())
        else:
            lex_list.append(error('IDENTIFIER', 'action_def'))
        if (scanner.lex[lex_en['value']] == 'USING' or
                scanner.lex[lex_en['value']] == 'LP'):
            lex_list.append(pusing_ref())
    # Following 'IF' path
    elif scanner.lex[lex_en['value']] == 'IF':
        scanner.next()
        lex_list.append(pcondition())
        if scanner.lex[lex_en['value']] == 'THEN':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
             lex_list.append(error('THEN', 'action_def'))
        lex_list.append(pactions())
        if scanner.lex[lex_en['value']] == 'ELSEIF':
            lex_list.append(ptest_elsif())
        if scanner.lex[lex_en['value']] == 'ELSE':
            lex_list.append(opt_else())
        if scanner.lex[lex_en['value']] == 'ENDIF':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('ENDIF', 'action_def'))
    # Following 'FOR' path
    elif scanner.lex[lex_en['value']] == 'FOR':
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
            lex_list.append(name_ref())
        else:
            lex_list.append(error('IDENTIFIER', 'action_def'))
        if scanner.lex[lex_en['value']] == 'EQUOP':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('EQUOP', 'action_def'))
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            lex_list.append(expr())
        else:
            lex_list.append(error('expr keyword', 'action_def'))
        if (scanner.lex[lex_en['value']] == 'TO' or
                scanner.lex[lex_en['value']] == 'DOWNTO'):
            lex_list.append(downto())
            scanner.next()
        else:
            lex_list.append(error('TO or DOWNTO', 'action_def'))
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            lex_list.append(expr())
        else:
            lex_list.append(error('expr keyword', 'action_def'))
        if scanner.lex[lex_en['value']] == 'DO':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('DO', 'action_def'))
        lex_list.append(pactions())
        if scanner.lex[lex_en['value']] == 'ENDFOR':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('ENDFOR', 'action_def'))
    # Following 'REPEAT' path
    elif scanner.lex[lex_en['value']] == 'REPEAT':
        scanner.next()
        lex_list.append(pactions())
        if scanner.lex[lex_en['value']] == 'UNTIL':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('UNTIL', 'action_def'))
        lex_list.append(pcondition())
        if scanner.lex[lex_en['value']] == 'ENDREPEAT':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('ENDREPEAT', 'action_def'))
    # Following 'WHILE' path
    elif scanner.lex[lex_en['value']] == 'WHILE':
        scanner.next()
        lex_list.append(pcondition())
        if scanner.lex[lex_en['value']] == 'DO':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('DO', 'action_def'))
        lex_list.append(pactions())
        if scanner.lex[lex_en['value']] == 'ENDWHILE':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('ENDWHILE', 'action_def'))
    # Following 'CASE' path
    elif scanner.lex[lex_en['value']] == 'CASE':
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
            lex_list.append(name_ref())
        else:
            lex_list.append(error('IDENTIFIER', 'action_def'))
        if scanner.lex[lex_en['value']] == 'MWHEN':
            lex_list.append(pcase_val())
        else:
            lex_list.append(error('MWHEN', 'action_def'))
        if scanner.lex[lex_en['value']] == 'DEFAULT':
            lex_list.append(pcase_def())
        if scanner.lex[lex_en['value']] == 'MENDCASE':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('MENDCASE', 'action_def'))
    # Following 'POSTCONDITION' path
    elif scanner.lex[lex_en['value']] == 'MEXIT':
        scanner.next()

    elif scanner.lex[lex_en['value']] == 'MBREAK':
        scanner.next()
    elif scanner.lex[lex_en['value']] == 'POSTCONDITION':
        scanner.next()
        lex_list.append(pcondition())
    # Default error
    else:
        lex_list.append(error('action_def keyword', 'action_def'))
    return lex_list

def name_ref():
    lex_list = ['name_ref']
    if (scanner.lex[lex_en['value']] == 'LB'):
        lex_list.append(opt_ref())
    else:
        lex_list.append(error('LB', 'name_ref'))
    if scanner.lex[lex_en['value']] == 'OF':
        lex_list.append(pmember_opt())
    if scanner.lex[lex_en['value']] == 'DOT':
        lex_list.append(popt_dot())
    return lex_list

def opt_ref():
    lex_list = ['opt_ref']
    lex_list.append(array_val())
    return lex_list

def pmember_opt():
    lex_list = ['pmember_opt']
    lex_list.append(pmember_of())
    return lex_list

def pmember_of():
    lex_list = ['pmember_of']
    lex_list.append(tuple(scanner.lex))
    scanner.next()
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        lex_list.append(error('IDENTIFIER', 'pmember_of'))
    if scanner.lex[lex_en['value']] == 'LB':
        lex_list.append(opt_ref())
    else:
        lex_list.append(error('LB', 'pmember_of'))
    while scanner.lex[lex_en['value']] == 'OF':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
        if scanner.lex[lex_en['value']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('IDENTIFIER', 'pmember_of'))
        if scanner.lex[lex_en['value']] == 'LB':
            lex_list.append(opt_ref())
        else:
            lex_list.append(error('LB', 'pmember_of'))
    else:
        return lex_list

def popt_dot():
    lex_list = ['popt_def']
    lex_list.append(proc_dot())
    return lex_list

def proc_dot():
    lex_list = ['proc_dot']
    lex_list.append(tuple(scanner.lex))
    scanner.next()
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        lex_list.append(error('IDENTIFIER', 'proc_dot'))
    if scanner.lex[lex_en['value']] == 'LB':
        lex_list.append((opt_ref()))
    else:
        lex_list.append(error('LB', 'proc_dot'))
    while scanner.lex[lex_en['value']] == 'DOT':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('IDENTIFIER', 'proc_dot'))
            return lex_list
        if scanner.lex[lex_en['value']] == 'LB':
            lex_list.append((opt_ref()))
        else:
            lex_list.append(error('LB', 'proc_dot'))
    else:
        return lex_list

def pvar_value_list():
    lex_list = ['pvar_value_list']
    # Valid types and values for following the expr() path
    valid_types = ['IDENTIFIER', 'STRING', 'LETTER', 'ICON', 'HCON', 'FCON']
    valid_values = ['MINUS', 'NEGATE', 'MTRUE', 'MFALSE', 'LP']
    while (scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values):
        lex_list.append(expr())
        if (scanner.lex[lex_en['value']] == 'COMMA'):
            lex_list.append(scanner.lex)
            scanner.next()
    return lex_list

def in_out():
    lex_list = ['in_out']
    lex_list.append(tuple(scanner.lex))
    scanner.next()
    if scanner.lex[lex_en['value']] == 'MFILE':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        lex_list.append(error('MFILE', 'in_out'))
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        lex_list.append(error('IDENTIFIER', 'in_out'))
    return lex_list

def read_write():
    lex_list = ['read_write']
    # Valid types and values for following the pvar_value_list() path
    valid_types = ['IDENTIFIER', 'STRING', 'LETTER', 'ICON', 'HCON', 'FCON']
    valid_values = ['MINUS', 'NEGATE', 'MTRUE', 'MFALSE', 'LP']
    lex_list.append(tuple(scanner.lex))
    scanner.next()
    if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
        lex_list.append(pvar_value_list())
    else:
        lex_list.append(error('pvar_value_list keyword', 'read_write'))
    if (scanner.lex[lex_en['value']] == 'FROM' or
            scanner.lex[lex_en['value']] == 'TO'):
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        lex_list.append(error('FROM or TO', 'read_write'))
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        lex_list.append(error('IDENTIFIER', 'read_write'))
    return lex_list

def pusing_ref():
    lex_list = ['pusing_ref']
    if scanner.lex[lex_en['value']] == 'USING':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
        lex_list.append(arg_list())
    elif scanner.lex[lex_en['value']] == 'LP':
        lex_list.append(parguments())
    else:
        lex_list.append(error('USING or LP', 'pusing_ref'))
    return lex_list

def ptest_elsif():
    lex_list = ['ptest_elsif']
    lex_list.append(proc_elseif())
    return lex_list

def proc_elseif():
    lex_list = ['proc_elseif']
    while scanner.lex[lex_en['value']] == 'ELSEIF':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
        lex_list.append(pcondition())
        if scanner.lex[lex_en['value']] == 'THEN':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('THEN', 'proc_elseif'))
        lex_list.append(pactions())
    return lex_list

def opt_else():
    lex_list = ['opt_else']
    lex_list.append(tuple(scanner.lex))
    scanner.next()
    lex_list.append(pactions())
    return lex_list

def downto():
    lex_list = ['downto']
    lex_list.append(tuple(scanner.lex))
    return lex_list

def pcase_val():
    lex_list = ['pcase_val']
    valid_types = ['IDENTIFIER', 'STRING', 'LETTER', 'ICON', 'HCON', 'FCON']
    valid_values = ['MINUS', 'NEGATE', 'MTRUE', 'MFALSE', 'LP']
    while scanner.lex[lex_en['value']] == 'MWHEN':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
        if (scanner.lex[lex_en['type']] in valid_types or
                scanner.lex[lex_en['value']] in valid_values):
            lex_list.append(expr())
        if scanner.lex[lex_en['value']] == 'COLON':
            lex_list.append(tuple(scanner.lex))
            scanner.next()
        else:
            lex_list.append(error('COLON', 'pcase_val'))
        lex_list.append(pactions())
    return lex_list

def pcase_def():
    lex_list = ['pcase_def']
    lex_list.append(tuple(scanner.lex))
    scanner.next()
    if scanner.lex[lex_en['value']] == 'COLON':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        lex_list.append(error('COLON', 'pcase_def'))
    lex_list.append(pactions())
    return lex_list

if __name__ == '__main__':
	program_start()
