'''
Parser.py
The parser uses the recursive-descent method of parsing, 
where each left hand definition is represented as a function.
The root of the parse tree is the function program. 
Each function calls the functions of the right hand components it is 
composed of. If there are multiple right hand definitions, they are attempted in order
Through this process, the data is collected by passing along an int called c_lex, lexeme_int
The original caller has a list called lexeme_list. lexeme_list is appended the return value of each function called.
Each of those functions call other subfunctions that will append the return value of the called function to their own lexeme_list.
However, there are two cases to consider. 
If there are multiple right hand definitions, only one will be correct. Sometimes, the wrong function will be chosen first and as a result nothing will be returned. 
If this is the case, then the integer current_lex needs to be reverted to its value before calling the function. 
The document has errors in it. If all right hand definitions are exhausted and none of them work (at a certain level), then an error message is created at some level
In this case, the c_lex value must not be reverted, because parsing must recover and continue. 
ISSUE: Where do we decide to put the error. Theoretically, it could be at the root of the tree. 
POSSIBLE SOLUTION: Certain definitions are considered "choke points for errors" like action_def. 
If one action_def in a pactions is malformed, the pactions should continue to process more action_defs.   
lexeme_list = a recursive list lexemes [lexeme[[sublexeme1[sub sub lexeme]] ... [sublexeme[sublexeme]]]]
ISSUE: When do we decide to add more lexemes to the initial pool of lexemes.
POSSIBLE SOLUTION: We call the scanner and get all of the lexemes at once. We then append Nothing to the end to signify the last lexeme has been read.
'''

''' 
Sorry for globals, but every function needs these, (unless we pass object?):
	global c_lex
	global t_lex
'''

c_lex = 0 #Count of lexemes
t_lex = [] # Array of lexemes


# Returns number of tabs
def returnTabs(tabNum):
	tabs = ''
	for(i = 0 in tabNum):
		tabs = tabs + '\t'
	return tabs 

# (WILL) prints tree; child nodes are indented with tabs
def printTree(tree_list):
	print('hi')

def program_start():
	global c_lex
	global t_lex
	lexeme_list = []
	lexeme_list.append(func_main())
	#lexeme_list.append(globals())
	#lexeme_list.appebd(implement())
	
def func_main():
	global c_lex
	global t_lex
	temp_c_lex = c_lex # Save the current value of c_lex in case something does not work
	lexeme_list = []
	# Check for Keyword FUNCTION, and go to next lexeme (next)
	# If FUNCTION is not found, check for MAIN instead and return that. 
	# Check for Keyword IDENTIFIER (next)
	# call function oper_type()
	return lexeme_list
	
	
def oper_type():
	global c_lex
	global t_lex
	temp_c_lex
	lexeme_list = []	
	# Check for RETURN
	# call chk_ptr
	# call chk_array
	# call ret_type
	
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
