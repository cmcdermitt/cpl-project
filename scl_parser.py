# Authors: Charlie McDermitt
#          Eric Schneider
#          Corey Harris
# Class:   CS4308 - W01
#          Concepts of Programming Languages
# Title:   Final Project - Second Deliverable
# Date:    09 July 2018

from scanner import Scanner
import sys
from parser_tree import Node

# The parser uses the recursive-descent method of parsing, where each left hand definition is represented as a function.
# The root of the parse tree is the function program.
# Each function calls the functions of the right hand components after checking if it is
# possible to use those components by looking ahead.
# The original caller has a list called lex_list. lex_list is appended
# the return value of each function called. Each return value is a list.
# Each of those functions in turn calls other subfunctions that will append
# the return value of the called function to their own lex_list.
# However, if there are multiple right hand definitions, only one will be correct, so the correct function must be chosen before we enter it.
# If the parser enncounters an error, it appends an error message instead of a list.

lex_en = {'type' : 1, 'value' : 0, 'line_num' : 2}
scanner = Scanner(sys.argv[1])


# Starting point for parser

# In general, each function checks the unique case that defines its particular grammar as defined by the document
# The general structure instantiates a new instance of lex_list, and sets its initial value to the name of the function
# This creates an easy to follow hierarchy and flow of function calls that can be read and debugged via the output
# The function then retrieves each subsequent lexeme from the symbol table, checks its validity, and adds it to lex_list
# Once the last lexeme has been appended the lex_list, it is returned and appended to the instance of the calling method
# If the function encounters an error, it appends an error message and skips over that lexeme.
# This method of error checking allows to catch each individual error without it crashing the entire system.
def parse():
    scanner.start()
    
    #node = pcondition()
    node = Node('Program')
    node.children.append(func_main())
    node.children.append(f_globals())
    node.children.append(implement())
    return node

    # lex_list = ['Program']
    # lex_list.append(func_main())

    # if(scanner.lex[lex_en['value']] == 'GLOBAL'):
    # 	lex_list.append(f_globals()) #called f_globals becasue globals is a function

    # lex_list.append(implement())
    # return lex_list


#convenience function returning an error message
#first parameter is what was expected, second is optional location
def error(expected, location = ''):
    print("***ERROR***")
    print(scanner.lex[lex_en['value']])
    if location == '':
        print ('Parser error: {} expected'.format(expected))
    else:
        print('Parser error: {} expected in {}'.format(expected, location))
    exit()

# First case: Called by parse()
# GRAMMAR: func_main ::= FUNCTION IDENTIFIER RETURN MVOID
#                   | MAIN
def func_main():
    # Append function header to output list
    node = Node('func_main')
    if(scanner.lex[lex_en['value']] == 'MAIN'):
        scanner.next()
        return node
    elif(scanner.lex[lex_en['value']] == 'FUNCTION'):
        scanner.next()
        if(scanner.lex[lex_en['type']] == 'IDENTIFIER'):
            node.children.append(scanner.lex[lex_en['value']])
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER', 'func_main')
        if(scanner.lex[lex_en['value']] == 'RETURN'):
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('RETURN', 'func_main')
        if(scanner.lex[lex_en['value']] == 'MVOID'):
            scanner.next()
        else:
            error('MVOID', 'func_main')
    else:
        # Append error message if case specific grammar not found
        error('MAIN or FUNCTION', 'func_main')
    return node

# CASE: globals
# GRAMMAR: globals ::= [GLOBAL DECLARATIONS const_var_struct]
# named f_globals() instead of globals() due to name conflicts
def f_globals():
    node = Node('f_globals')
    if scanner.lex[lex_en['value']] == 'GLOBAL':
        scanner.next()
        if(scanner.lex[lex_en['value']] == 'DECLARATIONS'):
            scanner.next()
        else:
            error('DECLARATIONS', 'f_globals')
        node.children.append(const_var_struct())
    return node

# CASE: const_dec
# GRAMMAR: const_dec ::= [CONSTANTS data_declarations]
def const_dec():
    node = Node('const_dec')
    if scanner.lex[lex_en['value']] == 'CONSTANTS':
        scanner.next()
        node.children.append(data_declarations())
    return node

# CASE: var_dec
# GRAMMAR: var_dec ::= VARIABLES data_declarations
def var_dec():
    node = Node('var_dec')
    if scanner.lex[lex_en['value']] == 'VARIABLES':
        scanner.next()
    else:
        error('VARIABLES', 'var_dec')
    
    node.children.append(data_declarations())
    return node

# CASE: data_declarations
# GRAMMAR: data_declarations ::=  DEFINE data_declaration {DEFINE data_declaration}
def data_declarations():
    node = Node('data_declarations')
    if scanner.lex[lex_en['value']] == 'DEFINE': #check validity before starting while loop
        while(scanner.lex[lex_en['value']] == 'DEFINE'):
            scanner.next()
            node.children.append(data_declaration())
    else:
        error('DEFINE', 'data_declarations')
    return node

# CASE: data_declaration
# GRAMMAR: data_declaration ::= IDENTIFIER [parray_dec] OF data_type
# This function is different than data_declarations
def data_declaration():
    # Append function header to output list
    node = Node('data_declaration')
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
    else:
        error('IDENTIFIER', 'data_declaration')
    node.children.append(parray_dec())
    if(scanner.lex[lex_en['value']] == 'OF'):
        scanner.next()
    else:
        error('OF', 'data_declaration')
    node.children.append(data_type())
    return node

# CASE: parray_dec
# GRAMMAR: parray_dec ::= ARRAY plist_const [popt_array_val]
def parray_dec():
    node = Node('parray_dec')
    if(scanner.lex[lex_en['value']] == 'ARRAY'):
        scanner.next()
        node.children.append(plist_const())
        node.children.append(popt_array_val())
    return node

# CASE: plist_const
# plist_const ::= LB (ICON | IDENTIFIER) RB { LB (ICON | IDENTIFIER) RB }
def plist_const():
    node = Node('plist_const')
    if scanner.lex[lex_en['value']] == 'LB':
        scanner.next()
    if(scanner.lex[lex_en['type']] == 'IDENTIFIER' or scanner.lex[lex_en['type']] == 'ICON'):
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
    else:
        error('IDENTIFIER or ICON', 'plist_const')
    if(scanner.lex[lex_en['value']] == 'RB'):
        scanner.next()
    else:
        error('RB', 'plist_const')
    while(scanner.lex[lex_en['value']] == 'LB'):
        scanner.next()
        if(scanner.lex[lex_en['type']] == 'IDENTIFIER' or scanner.lex[lex_en['type']] == 'ICON'):
            node.children.append(scanner.lex[lex_en['value']])
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER or ICON', 'plist_const')
        if (scanner.lex[lex_en['value']] == 'RB'):
            scanner.next()
        else:
            error('RB', 'plist_const')
    return node

# CASE: popt_array_val
# GRAMMAR: popt_array_val ::= (VALUE | EQUOP) array_val
def popt_array_val():
    # Append function header to output list
    node = Node('popt_array_val')
    if scanner.lex[lex_en['value']] == 'VALUE' or scanner.lex[lex_en['value']] == 'EQUOP':
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
        node.children.append(array_val())
    return node

# CASE: value_eq
# GRAMMAR: value_eq ::= VALUE
#						| EQUOP
def value_eq():
    # Append function header to output list
    lex_list = ['value_eq']
    if scanner.lex[lex_en['value']] == 'EQUOP' or scanner.lex[lex_en['value']] == 'VALUE':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        # Append error message if case specific grammar not found
        lex_list.append(error('EQUOP or VALUE', 'value_eq'))
    return lex_list

# CASE: array_val
# GRAMMAR: LB arg_list RB
def array_val():
    # Append function header to output list
    node = Node('array_val')
    if scanner.lex[lex_en['value']] == 'LB':
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
    else:
        error('LB', 'array_val')
    lex_list.append(arg_list())
    if(scanner.lex[lex_en['value']] == 'RB'):
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
    else:
        error('RB', 'array_val')
    return node

# CASE: arg_list
# GRAMMAR: arg_list ::= expr {COMMA expr}
def arg_list():
    # Append function header to output list
    node = Node('arg_list')
    node.children.append(expr())
    while (scanner.lex[lex_en['value']] == 'COMMA'):
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
        node.children.append(expr())
    return node

# CASE: data_type
# Grammar: data_type ::= TUNSIGNED
#						 | CHAR
#						 | INTEGER
#						 | MVOID
#						 | DOUBLE
#						 | LONG
#						 | SHORT
#						 | FLOAT
#						 | REAL
#						 | TSTRING
#						 | TBOOL
#						 | TBYTE
def data_type():
    node = Node('data_type')
    valid_types = ['TUNSIGNED', 'CHAR', 'INTEGER', 'MVOID', 'DOUBLE', 'LONG',
                    'SHORT', 'FLOAT', 'REAL', 'TSTRING', 'TBOOL', 'TBYTE']
    if scanner.lex[lex_en['value']] in valid_types:
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
    else:
        error('valid type', 'data_type')
    return node

# CASE: expr
# GRAMMAR: expr ::= term [ (PLUS | MINUS | BAND | BOR | BXOR) term ]

def expr():
    #process the first <term>, but don't add it to a node yet
    first_term = term() 

    #check whether there are multiple terms
    this_lex = scanner.lex[lex_en['value']]
    if (this_lex == 'PLUS' or this_lex == 'MINUS' or this_lex == 'BAND' or this_lex == 'BOR' or this_lex == 'BXOR'):

        node = Node(this_lex)
        node.children.append(first_term)
        scanner.next()

        node.children.append(term())
    else:
        node = first_term
    return node

    

# CASE: term
# GRAMMAR: term ::= punary [ (STAR | DIVOP | MOD | LSHIFT | RSHIFT) punary]
def term():

    # Append function header to output list
    first_punary = punary()
    this_lex = scanner.lex[lex_en['value']]
    if (this_lex == 'STAR' or this_lex == 'DIVOP' or this_lex == 'MOD' or this_lex == 'LSHIFT' or this_lex == 'RSHIFT'):
        node = Node(this_lex)

        node.children.append(first_punary)
        scanner.next()

        node.children.append(punary())
    else:
        node = first_punary
    return node

# CASE: punary
# GRAMMAR: punary ::= [NEGATE] element
def punary():

    # Append function header to output list
    if scanner.lex[lex_en['value']] == 'NEGATE':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        node.children.append(element())
    else:
        node = element()
    return node

# CASE: element
# GRAMMAR: element ::= IDENTIFIER [(array_val | parguments)]
#     | STRING
#     | LETTER
#     | ICON
#     | HCON
#     | FCON
#     | MTRUE
#     | MFALSE
#     | LP expr RP
def element():
    # Append function header to output list
    valid_types = ['STRING', 'LETTER', 'ICON', 'HCON', 'FCON', 'IDENTIFIER']
    valid_values = ['MTRUE', 'MFALSE']
    if scanner.lex[lex_en['type']] in valid_types: #needs additional code for identifier if using arrays
        node = Node(scanner.lex[lex_en['type']], scanner.lex[lex_en['value']])
        scanner.next()
    elif scanner.lex[lex_en['value']] in valid_values:
        node = Node('BOOL', scanner.lex[lex_en['value']])
        scanner.next()

        # for arrays
        # if scanner.lex[lex_en['value']] == 'LB':
        # 	lex_list.append(popt_ref())
    elif scanner.lex[lex_en['value']] == 'LP':
        scanner.next()
        node = expr()
        if scanner.lex[lex_en['value']] == 'RP':
            scanner.next()
        else:
            error('RP', 'element')
    else:
        # Append error message if case specific grammar not found
        error('IDENTIFIER or LP or TYPE or MTRUE or MFALSE', 'element')
    return node

# CASE: popt_ref
# GRAMMAR: popt_reg ::=
#						| array_val
#						| parguments
# NOTE: Blank line interpreted as optional input valuues
def popt_ref():
    # Append function header to output list
    lex_list = ['popt_ref']
    if scanner.lex[lex_en['value']] == 'LB':
        lex_list.append(array_val())
    elif scanner.lex[lex_en['value']] == 'LP':
        lex_list.append(parguments())
    else:
        return lex_list
    return lex_list

# CASE: parguments
# GRAMMAR: LP arg_list RP
def parguments():
    # Append function header to output list
    lex_list = ['parguments']
    if scanner.lex[lex_en['value']] == 'LP':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        # Append error message if case specific grammar not found
        lex_list.append(error('LP', 'parguments'))
    lex_list.append(arg_list())
    if scanner.lex[lex_en['value']] == 'RP':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        # Append error message if case specific grammar not found
        lex_list.append(error('RP', 'parguments'))
    return lex_list

# CASE: implement
# GRAMMAR: implement ::= IMPLEMENTATIONS [MAIN DESCRIPTION parameters] funct_list

def implement():
    node = Node('implement')
    if scanner.lex[lex_en['value']] == 'IMPLEMENTATIONS':
        scanner.next()
    else:
        error('IMPLEMENTATIONS', 'implement')
    if scanner.lex[lex_en['value']] == 'MAIN':
        scanner.next()
        if scanner.lex[lex_en['value']] == 'DESCRIPTION':
            scanner.next()
            node.children.append(parameters())
        else:
            error('DESCRIPTION', 'implement')
    node.children.append(funct_list())
    return node

# CASE: main_head
# GRAMMAR: main_head ::=
#						| MAIN DESCRIPTION parameters
# NOTE: Blank line in first line interpreted as optional value
def main_head():
    # Append function header to output list
    lex_list = ['main_head']
    if scanner.lex[lex_en['value']] == 'MAIN':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        return lex_list
    if scanner.lex[lex_en['value']] == 'DESCRIPTION':
        lex_list.append(tuple(scanner.lex))
        scanner.next()
    else:
        # Append error message if case specific grammar not found
        lex_list.append(error('DESCRIPTION','main_head'))
    lex_list.append(parameters())
    return lex_list

# CASE: parameters
# GRAMMAR: parameters ::= [PARAMETERS data_declaration {COMMA data_declaration}]
def parameters():
    node = Node('parameters')
    if scanner.lex[lex_en['value']] == 'PARAMETERS':
        scanner.next()
        node.children.append(data_declaration())
        while scanner.lex[lex_en['value']] == 'COMMA':
            scanner.next()
            node.children.append(data_declaration())
    return node

# CASE: param_def
# GRAMMAR: param_def ::= data_declaration
def param_def():
    # Append function header to output list
    lex_list = ['param_def']
    lex_list.append(data_declaration())
    return lex_list

# CASE: funct_list
# GRAMMAR: funct_list ::= FUNCTION pother_oper_def { FUNCTION pother_oper_def }
def funct_list():
    node = Node('funct_list')
    
    if scanner.lex[lex_en['value']] == 'FUNCTION': #check validity before loop
        while scanner.lex[lex_en['value']] == 'FUNCTION':
            scanner.next()
            node.children.append(pother_oper_def())
    else:
        error('FUNCTION', 'pother_oper_def')
    return node

# CASE: pother_oper_def
# GRAMMAR: pother_oper_def ::= IDENTIFIER DESCRIPTION parameters IS const_var_struct BEGIN pactions ENDFUN IDENTIFIER
def pother_oper_def():
    # Append function header to output list
    node = Node('pother_oper_def')
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
    else:
        error('IDENTIFIER', 'pother_oper_def')

    if scanner.lex[lex_en['value']] == 'DESCRIPTION':
        scanner.next()
    else:
        error('DESCRIPTION', 'pother_oper_def')

    node.children.append(parameters())

    if scanner.lex[lex_en['value']] == 'IS':
        scanner.next()
    else:
        error('IS', 'pother_oper_def')

    node.children.append(const_var_struct())

    if scanner.lex[lex_en['value']] == 'BEGIN':
        scanner.next()
    else:
        error('BEGIN', 'pother_oper_def')
    node.children.append(pactions())
    if scanner.lex[lex_en['value']] == 'ENDFUN':
        scanner.next()
    else:
        error('ENDFUN', 'pother_oper_def')
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
    else:
        error('IDENTIFIER', 'pother_oper_def')
    return node

#CASE const_var_struct
#GRAMMAR ::= const_var_struct ::= const_dec var_dec struct_dec
def const_var_struct():
    # Append function header to output list
    node = Node('const_var_struct')
    node.children.append(const_dec())
    node.children.append(var_dec())
    return node

#CASE pcondition
#GRAMMAR pcond1 [(OR | AND) pcond1]
def pcondition():
    # Append function header to output list
    first_pcond1 = pcond1()
    word = scanner.lex[lex_en['value']]
    if word == 'OR' or word == 'AND':
        node = Node(scanner.lex[lex_en['value']])
        node.children.append(first_pcond1)
        scanner.next()
        node.children.append(pcond1())
    else:
        node = first_pcond1
    return node

#CASE pcond1
#GRAMMAR [NOT] pcond2
def pcond1():
    if scanner.lex[lex_en['value']] == 'NOT':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        node.children.append(pcond2())
    else:
        node = pcond2()
    return node

# CASE pcond2
#  GRAMMAR pcond2 ::= LP pcondition RP
#     | expr eq_v expr
#     | [NOT] (MTRUE | MFALSE)
#     | expr
def pcond2():
    # Append function header to output list
    # For LP pcondition RP case
    if scanner.lex[lex_en['value']] == 'LP':
        scanner.next()
        
        print(scanner.lex[lex_en['value']])
        node = pcondition()
        print(scanner.lex[lex_en['value']])
        if scanner.lex[lex_en['value']] == 'RP':
            scanner.next()
        else:
            error('RP', 'pcond2')

    elif scanner.lex[lex_en['value']] == 'NOT':
        node = Node('NOT')
        scanner.next()
        if scanner.lex[lex_en['value']] == 'MTRUE' or scanner.lex[lex_en['value']] == 'MFALSE':
            node.children.append(Node(scanner.lex[lex_en['type']], scanner.lex[lex_en['value']]))
            scanner.next()
        else:
            error('MTRUE or MFALSE', 'pcond2')

    elif scanner.lex[lex_en['value']] == 'MTRUE' or scanner.lex[lex_en['value']] == 'MFALSE':
        node = Node(scanner.lex[lex_en['type']], scanner.lex[lex_en['value']])
        scanner.next()

    else:
        first_expr = expr()
        word = scanner.lex[lex_en['value']]
        if(word == 'EQUALS' or word == 'GREATER' or word == 'LESS'):
            node = eq_v()
            node.children.append(first_expr)
            node.children.append(expr())
        else:
            node = first_expr
    return node


#CASE eq_v
#GRAMMAR ::=  EQUALS
#			| GREATER THAN
#			| LESS THAN
#			| GREATER OR EQUAL
#			| LESS OR EQUAL
def eq_v():
    word = scanner.lex[lex_en['value']]
    if(word == 'EQUALS'):
        node = Node('EQUALS')
        scanner.next()
    elif(word == 'GREATER' or word == 'LESS'):
        scanner.next()
        if(scanner.lex[lex_en['value']] == 'THAN'):
            node = Node (word + ' ' + scanner.lex[lex_en['value']])
            scanner.next()
        elif scanner.lex[lex_en['value']] == 'OR':
            scanner.next()
            if scanner.lex[lex_en['value']] == 'EQUAL':
                node = Node (word + ' OR ' + scanner.lex[lex_en['value']])
                scanner.next()
            else:
                error('EQUAL', 'eq_v')
        else:
            # Append error message if case specific grammar not found
            error('THAN or OR', 'eq_v')
    else:
        error('EQUALS, GREATER, or LESS', 'eq_v')
    return node

#CASE pactions
#GRAMMAR  pactions ::= action_def {action_def}
def pactions():
    # Append function header to output list
    print (scanner.lex[lex_en['value']])
    valid_values = ['SET', 'READ', 'INPUT', 'DISPLAY', 'DISPLAYN',
                    'INCREMENT', 'DECREMENT', 'RETURN', 'CALL', 'IF', 'FOR', 'REPEAT',
                    'WHILE', 'CASE', 'MBREAK', 'MEXIT','POSTCONDITION', 'THEN', 'DO']
    if scanner.lex[lex_en['value']] not in valid_values:
        #print(scanner.lex[lex_en['value']])
        error('action_def keyword', 'pactions')
    node = Node('pactions')
    while scanner.lex[lex_en['value']] in valid_values:
        node.children.append(action_def())
        
    return node

# CASE action_def
#GRAMMAR action_def ::= SET name_ref EQUOP exp
#						| READ pvar_value_list
#						| INPUT name_ref
#						| DISPLAY pvar_value_list
#						| DISPLAYN pvar_value_list
#						| INCREMENT name_ref
#						| DECREMENT name_ref
#						| RETURN expr
#						| CALL name_ref pusing_ref
#						| IF pcondition THEN pactions ptest_elsif opt_else ENDIF
#						| FOR name_ref EQUOP expr downto expr DO pactions ENDFOR
#						| REPEAT pactions UNTIL pcondition ENDREPEAT
#						| WHILE pcondition DO pactions ENDWHILE
#						| CASE name_ref pcase_val pcase_def MENDCASE
#						| MBREAK
#						| MEXIT
#						| ENDFUN name_ref
#						| POTCONDITION pcondition

def action_def():
    # Append function header to output list
    
    # Valid types and values for following the expr() path
    valid_types = ['IDENTIFIER', 'STRING', 'LETTER', 'ICON', 'HCON', 'FCON']
    valid_values = ['MINUS', 'NEGATE', 'MTRUE', 'MFALSE', 'LP']

    # Determine path of execution for action_def group
    # Following 'SET' path
    if scanner.lex[lex_en['value']] == 'SET':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            node.children.append(name_ref())
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER','action_def CASE SET')
        if scanner.lex[lex_en['value']] == 'EQUOP':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('EQUOP', 'action_def')
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            node.children.append(expr())
        else:
            # Append error message if case specific grammar not found
            error('expr keyword', 'action_def')
    # Following 'INPUT' path
    elif scanner.lex[lex_en['value']] == 'INPUT':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            node.children.append(name_ref())
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER', 'action_def')
    # Following 'DISPLAY' or 'DISPLAYN' path
    elif (scanner.lex[lex_en['value']] == 'DISPLAY'):
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            node.children.append(arg_list())
        else:
            # Append error message if case specific grammar not found
            error('expr keyword', 'action_def')
    # Following 'INCREMENT' or 'DECREMENT' path
    elif (scanner.lex[lex_en['value']] == 'INCREMENT' or
            scanner.lex[lex_en['value']] == 'DECREMENT'):
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            node.children.append(name_ref())
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER', 'action_def')
    ## Following 'RETURN' path
    #elif scanner.lex[lex_en['value']] == 'RETURN':
     #   scanner.next()
      #  if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
       #     lex_list.append(expr())
        #else:
            # Append error message if case specific grammar not found
            error('expr keyword', 'action_def')
    # Following 'CALL' path
    elif scanner.lex[lex_en['value']] == 'CALL':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            node.children.append(name_ref())
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER', 'action_def')
        node.children.append(pusing_ref())
    # Following 'IF' path
    elif scanner.lex[lex_en['value']] == 'IF':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        node.children.append(pcondition())
        if scanner.lex[lex_en['value']] == 'THEN':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
             error('THEN', 'action_def')
        node.children.append(pactions())
        if scanner.lex[lex_en['value']] == 'ELSEIF':
            node.children.append(ptest_elsif())
        if scanner.lex[lex_en['value']] == 'ELSE':
            scanner.next()
            node.children.append(pactions())
        if scanner.lex[lex_en['value']] == 'ENDIF':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('ENDIF', 'action_def')
    # Following 'FOR' path
    elif scanner.lex[lex_en['value']] == 'FOR':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            node.children.append(name_ref())
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER', 'action_def')
        if scanner.lex[lex_en['value']] == 'EQUOP':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('EQUOP', 'action_def')
        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            node.children.append(expr())
        else:
            # Append error message if case specific grammar not found
            error('expr keyword', 'action_def')

        if scanner.lex[lex_en['value']] == 'DOWNTO' or scanner.lex[lex_en['value']] == 'TO':
            node.children.append(Node(scanner.lex[lex_en['value']], 'KEYWORD'))
            scanner.next()

        if scanner.lex[lex_en['type']] in valid_types or scanner.lex[lex_en['value']] in valid_values:
            node.children.append(expr())
        else:
            # Append error message if case specific grammar not found
            error('expr keyword', 'action_def')
        if scanner.lex[lex_en['value']] == 'DO':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('DO', 'action_def')
        node.children.append(pactions())
        if scanner.lex[lex_en['value']] == 'ENDFOR':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('ENDFOR', 'action_def')
    # Following 'REPEAT' path
    elif scanner.lex[lex_en['value']] == 'REPEAT':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        node.children.append(pactions())
        if scanner.lex[lex_en['value']] == 'UNTIL':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('UNTIL', 'action_def')
        node.children.append(pcondition())
        if scanner.lex[lex_en['value']] == 'ENDREPEAT':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('ENDREPEAT', 'action_def')
    # Following 'WHILE' path
    elif scanner.lex[lex_en['value']] == 'WHILE':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        node.children.append(pcondition())
        if scanner.lex[lex_en['value']] == 'DO':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('DO', 'action_def')
        node.children.append(pactions())
        if scanner.lex[lex_en['value']] == 'ENDWHILE':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('ENDWHILE', 'action_def')
    # Following 'CASE' path
    elif scanner.lex[lex_en['value']] == 'CASE':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
        if scanner.lex[lex_en['type']] == 'IDENTIFIER':
            node.children.append(name_ref())
        else:
            # Append error message if case specific grammar not found
            error('IDENTIFIER', 'action_def')
        node.children.append(pcase_val())
        node.children.append(pcase_def())
        if scanner.lex[lex_en['value']] == 'MENDCASE':
            scanner.next()
        else:
            # Append error message if case specific grammar not found
            error('MENDCASE', 'action_def')
    # Following 'POSTCONDITION' path
    elif scanner.lex[lex_en['value']] == 'MEXIT':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
    elif scanner.lex[lex_en['value']] == 'MBREAK':
        node = Node(scanner.lex[lex_en['value']])
        scanner.next()
    # Default error
    else:
        # Append error message if case specific grammar not found
        error('action_def keyword', 'action_def')
    return node

#CASE name_ref
#GRAMMAR name_ref ::= IDENTIFIER array_val
def name_ref():
    node = Node('name_ref')
    # Append function header to output list
    print(scanner.lex[lex_en['value']])
    if scanner.lex[lex_en['type']] == 'IDENTIFIER':
        node.children.append(scanner.lex[lex_en['value']])
        scanner.next()
        if (scanner.lex[lex_en['value']] == 'LB'):
            node.children.append(array_val)
    else:
        error('IDENTIFIER', 'name_ref')
    return node

#CASE pusing_ref
#GRAMMAR pusing_ref ::= [( USING arg_list | LP arg_list RP)]
def pusing_ref():
    node = Node('pusing_ref')
    if scanner.lex[lex_en['value']] == 'USING':
        scanner.next()
        node.children.append(arg_list())
    elif scanner.lex[lex_en['value']] == 'LP':
        scanner.next()
        node.children.append(arg_list())
        if scanner.lex[lex_en['value']] == 'RP':
            scanner.next()
        else:
            error('RP', 'pusing_ref')
    return node

#CASE ptest_elsif
#GRAMMAR ptest_elsif ::= { ELSEIF pcondition THEN pactions }

def ptest_elsif():
    node = Node('ptest_elsif')
    while scanner.lex[lex_en['value']] == 'ELSEIF':
        scanner.next()
        node.children.append(pcondition())
        if scanner.lex[lex_en['value']] == 'THEN':
            scanner.next()
            node.children.append(pactions())
        else:
            error('THEN', 'ptest_elsif')
    return node

#CASE: pcase_val
#GRAMMAR: pcase_val ::= MWHEN expr COLON pactions {MWHEN expr COLON pactions}
def pcase_val():
    node = Node('pcase_val')

    if scanner.lex[lex_en['value']] == 'MWHEN':
        while scanner.lex[lex_en['value']] == 'MWHEN':
            scanner.next()
            node.children.append(expr())
            if scanner.lex[lex_en['value']] == 'COLON':
                scanner.next()
            else:
                error('COLON', 'pcase_val')
            node.children.append(pactions())
    else:
        error('MWHEN', 'pcase_val')
    return node

#CASE: pcase_def
#GRAMMAR: pcase_def ::= [DEFAULT COLON pactions]
def pcase_def():
    node = Node('pcase_def')
    if scanner.lex[lex_en['value']] == 'DEFAULT':
        scanner.next()
        if scanner.lex[lex_en['value']] == 'COLON': # Check if next lexeme is COLON
            scanner.next()
            node.children.append(pactions())
        else:
            error('COLON', 'pcase_def')
    return node