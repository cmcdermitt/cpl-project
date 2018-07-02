from enum import Enum

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


lex_en = {'ID' : 0, 'Pos' : 1, 'type' : 2, 'value': 3}

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
	print(returnTabs(tab) + tree_list[0])
	if(len(tree_list) == 1):
		return
	for x in range(1,len(tree_list)):
		if(isinstance(tree_list[x], str)):
			print(returnTabs(tab) + tree_list[x])
		else:
			printTree(tree_list[x],tab + 1)
	

# Starting point for parse tree 
# Initially, lex_list is ['Program']
# After appending func_main(), lex_list might be ['Program',[func_main, ['0','0','KEYWORD','FUNCTION'], ['1','1',IDENTIFER, 'MAIN'], [oper_type,['2','2','KEYWORD','RETURN']]]]
# The second pair of braces represents the entirety of func_main
# The third pair in this case, represents the individual lexeme (there could be more in this list)
def program_start():
	lex_list = ['Program']
	lex_list.append(func_main())
	printTree(lex_list, 0)
	print(lex_list)
	
def func_main():
	
	lex_list = ['func_main']
	lex = nextLex()
	if(lex[lex_en['value']] == 'MAIN'):
		lex_list.append(lex)
		lex_list.append(oper_type())
		return lex_list
	elif(lex[lex_en['value']] == 'FUNCTION'):
		lex_list.append(lex)
		lex = nextLex()
		if(lex[lex_en['type']] == 'IDENTIFIER'):
			lex_list.append(lex)
			lex = nextLex()
		else:
			lex_list.append(['Error: Identifer was expected'])
		if(lex[lex_en['value']] == 'RETURN'):
			lex_list.append(oper_type())
		else:
			lex_list.append(['Error: Keyword Return was expected'])
	else:
		lex_list.append(['Error Main function missing'])
	return lex_list
	
	
def oper_type():
	lex_list = ['oper_type']	
	lex_list.append(currentLex())
	lex = nextLex()
	if(lex[lex_en['value']] == 'POINTER'):
		lex_list.append(chk_ptr())
		lex = nextLex()
	if(lex[lex_en['value']] == 'ARRAY'):
		lex_list.append(chk_array)
		lex = nextLex()
	# Not done yet
	return lex_list
	
	
def chk_ptr():
	global c_lex
	global t_lex
	temp_c_lex
	lexeme_list = []	
	
def chk_array():
	global c_lex
	global t_lex
	temp_c_lex
	lexeme_list = []	
	
def ret_type():
	global c_lex
	global t_lex
	temp_c_lex
	lexeme_list = []	
	
def array_dim_list():
	global c_lex
	global t_lex
	temp_c_lex
	lexeme_list = []
	
def arrayIndex():
	global c_lex
	global t_lex
	temp_c_lex
	lexeme_list = []
	
def type_name():
	global c_lex
	global t_lex
	temp_c_lex
	lexeme_list = []
	
program_start()
