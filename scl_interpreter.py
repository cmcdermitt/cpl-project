# Then we add all of the global variables to the globals dictionary
import scl_var_table
# Then we execute the main function. <- done in implement

global_vars = scl_var_table.VarTable()
main_vars = scl_var_table.VarTable()
controlHeads = []
breakCalled = False


def error(msg, location = ''):
    if location == '':
        print ('Interpreter error: {}'.format(msg))
    else:
        print('Interpreter error: {} in {}'.format(msg, location))
    exit()

def lookup(var_name, local_scope = None):
    if var_name[0] == '\"':
        return var_name

    if local_scope is not None:
        if local_scope.isDeclared(var_name):
            return local_scope.getValue(var_name)
        if global_vars.isDeclared(var_name):
            return global_vars.isDeclared(var_name)
    elif global_vars.isDeclared(var_name):
        return global_vars.getValue(var_name)
    else:
        error('variable {} is undeclared and cannnot be looked up'.format(var_name), 'lookup')

# Main interpreter function
# Name: processNode(node)
# Summary: The processNode function is invoked by the main file after the parser has
#          generated the tree based on the input data.
#          The purpose of the interpret function is recognize keywords and parsed functions
#          and call corresponding functions based on the value.
#          Each function will receive a subtree containing the nodes from that keyword down,
#          and will set the new starting node after it has finished processing any related nodes
# Return: No output currently
def processNode(node):
    print('processing {} node {}'.format(node.type, node.value))
    nodeType = node.type.upper()
    if node.type.upper() == 'KEYWORD':
        nodeType = node.value.upper() #for MTRUE and MFALSE
    if nodeType in interpreterDict:
        funct = interpreterDict[nodeType]
        node = funct(node)
    return node

# Expected Structure:
# Type: INPUT
# Children: IDENTIFIER
def f_input(node):
    # Get associated identifier
    inputValue = node.children[0]
    # Add identifier to variable table
    main_vars.declare(inputValue)
    # output results
    print('Variable ' + inputValue + ' was declared')
    global_vars.declare(inputValue)
    # Node has no children -> IDENTIFIER is just a string
    # Return node to processNode
    return node

# Expected Structure:
# Type: DISPLAY or DISPLAYN
# Children: IDENTIFIER
def f_display(node):
    nodeType = node.type
    # Get IDENTIFIER value
    nodeValue = node.children[0]
    outputVal = main_vars.getValue(nodeValue)
    # Output results
    print(outputVal)
    # Node has no children -> IDENTIFIER is just a string
    return node

# Expected Structure:
# Type: INCREMENT
# Children: name_ref => IDENTIFIER
def f_increment(node):
    # Get node type
    nodeType = node.type
    # Get IDENTIFIER variable
    var = node.children[0]
    # Get value
    val = main_vars.getValue(var)
    # Increment and assign
    val = val + 1
    main_vars.assign(var, val)
    return node

# Expecred Structure:
# Type: DECREMENT
# Children: name_ref => IDENTIFIER
def f_decrement(node):
    # Get node type
    nodeType = node.type
    # Get IDENTIFIER variable
    var = node.children[0]
    # Get value
    val = main_vars.getValue(var)
    # Decrement and assign
    val = val - 1
    main_vars.assign(var.value, val)
    return node

# Expected Structure:
# Type: FOR
# Children: name_ref, expr, ( TO | DOWNTO ), expr, pactions
def f_for(node):
    global breakCalled
    # Get node type
    nodeType = node.type
    # Get IDENTIFIER
    nodeID = processNode(node.children[0])
    # Get corresponding Python variable
    var = lookup(nodeID)
    # Get first expr of for loop
    expr1 = processNode(node.children[1])
    # Perform lookup if type string to get value
    if isinstance(expr1, str):
        expr1 = lookup(expr1)
    # Determine if direction is TO or DOWNTO
    dir = node.children[2].value
    # Get second expr of for loop
    expr2 = processNode(node.children[3])
    # Perform lookup if type string to get value
    if isinstance(expr2, str):
        expr2 = lookup(expr2)
    # Assign initial value to IDENTIFIER
    main_vars.assign(nodeID, expr1)
    # Perform for loop up or down
    if dir == 'TO':
        while var < expr2:
            # Process pactions each time
            p = processNode(node.children[id])
            if breakCalled == True:
                breakCalled = False
                return node
            # Increment and assign
            var += 1
            main_vars.assign(nodeID, var)
    else:
        while var > expr2:
            # Perform pactions each time
            p = processNode(node.children[id])
            if breakCalled == True:
                breakCalled = False
                return node
            # Decrement and assign
            var -= 1
            main_vars.assign(nodeID, var)
    return node

# Type AND
# Children: pcond1 and pcond 1 or pcond 1 
def f_and(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    if len(node.children) > 1:
        arg2 = processNode(node.children[1])
        if isinstance(arg2, str):
            arg2 = lookup(arg2)
        return arg1 and arg2

# Expected Structure:
# Type: REPEAT
# Children pactions, pcondition
def f_repeat(node):
    global breakCalled
    # Get node type
    nodeType = node.type
    # Emulate a do-while by executing pactions once,
    # and repeating in while loop until conditional is false
    #
    # Perform initial pactions statement
    p = processNode(node.children[0])
    # Get pcondition
    cond = processNode(node.children[1])
    # Start while loop
    while cond:
        p = processNode(node.children[0])
        if breakCalled == True:
            breakCalled = False
            return node
        cond = processNode(node.children[1])
    return node

# Expected Structure:
# Type: WHILE
# Children pcondition, pactions
def f_while(node):
    global breakCalled
    # Get node type:
    nodeType = node.type
    # Get pcondition
    cond = processNode(node.children[1])
    # Start while loop
    while cond:
        p = processNode(node.children[0])
        if breakCalled == True:
            breakCalled = False
            return node
        cond = processNode(node.children[1])
    return node

# Expected Structure:
# Type: MBREAK
# Children: none
def f_mbreak(node):
    node = controlHeads.pop()
    return node

# Expected Structure:
# Type: MEXIT
# Children: none
def f_mexit(node):
    exit()

# Expected Structure:
# Type: CALL
# Children: name_ref => IDENTIFIER
def f_call(node):
    # Get node type
    nodeType = node.type
    for child in node.children:
        if isinstance(child, node):
            processNode(child)
        else:
            callValue = main_vars.getValue(node.children[0])
            print(callValue)
    return node


# Expected Structure:
# Type OR
# Children: pcond1 and pcond 1 or pcond 1
def f_or(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    if len(node.children) > 1:
        arg2 = processNode(node.children[1])
        if isinstance(arg2, str):
            arg2 = lookup(arg2)
        return arg1 or arg2
    else:
        return arg1

#Expected Structure
#TYPE NOT
#Children: Expr
def f_not(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    return arg1

# Expected Structure:
# Type MTRUE
# Children: None returns True
def f_mtrue(node):
    return True

# Expected Structure:
# Type MFALSE
# Children: None and returns False
def f_mfalse(node):
    return False 

# Expected Structure:
# Type Equal
# Children: expr, expr
def f_equals(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 == arg2

# Expected Structure:
# Type greater_than
# Children: expr, expr
def f_greater_than(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)     
    return arg1 > arg2

# Expected Structure:
# Type less_than
# Children: expr, expr
def f_less_than(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 < arg2

# Expected Structure:
# Type greater_or_equal
# Children: expr, expr
def f_greater_or_equal(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    arg1 >= arg2

# Expected Structure:
# Type less_or_equal
# Children: expr, expr

def f_less_or_equal(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 <= arg2 

def f_plus(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    return arg1 + arg2 

def f_minus(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 - arg2

def f_band(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 & arg2

def f_bor(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 | arg2 

def f_bxor(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 ^ arg2

def f_star(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 * arg2

def f_divop(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)

    if isinstance(arg1, int) and isinstance(arg2, int):
        return arg1 // arg2 #floor division
    else:
        return arg1 / arg2 #normal division

def f_mod(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 % arg2 

def f_lshift(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 << arg2

def f_rshift(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    arg2 = processNode(node.children[1])
    if isinstance(arg2, str):
        arg2 = lookup(arg2)
    return arg1 >> arg2 

def f_negate(node):
    arg = processNode(node.children[0])
    if isinstance(arg, str):
        arg = lookup(arg)
    return -arg

def f_icon(node):
    return int(node.value)

# def arg_list(node):
#     for child in node.children:
#         if child is nodes

# Expected structure:
# Type: pcase_def
# Children: pactions
def f_pcase_def():
    processNode(node.children[0])



interpreterDict = {
    'INPUT': f_input,
    'MFALSE': f_mfalse,
    'PCASE_DEF':f_pcase_def,
    'NEGATE': f_negate,
    'PLUS': f_plus,
    'MINUS': f_minus,
    'BOR' : f_bor,
    'BAND' : f_band,
    'BXOR' : f_bxor,
    'STAR' : f_star,
    'DIVOP' : f_divop,
    'LSHIFT' : f_lshift,
    'RSHIFT' : f_rshift,
    'MOD' : f_mod,
    'MTRUE' : f_mtrue,
    'EQUALS' : f_equals,
    'GREATER THAN' : f_greater_than,
    'GREATER OR EQUAL' : f_greater_or_equal,
    'LESS THAN' : f_less_than,
    'LESS OR EQUAL' : f_less_or_equal,
    'AND' : f_and,
    'OR' : f_or,
    'NOT' : f_not,
    'ICON' : f_icon
}

#     'DISPLAY'
#     'CALL'
#     'INCREMENT'
#     'DECREMENT'
#     'IFELSE'
#     'FORLOOP'
#     'WHILELOOP'
#     'CASE'
#     'REPEATLOOP'
#     'MBREAK'
#     'MEXIT'
#     'AND'
#     'OR'
#     'NOT'
#     'MTRUE'
#     'MFALSE'
#     'EQUALS'
#     'GREATERTHAN'
#     'LESSTHAN'
#     'GREATEROREQUAL'
#     'PLUS'
#     'MINUS'
#     'BAND'
#     'BOR'
#     'BXOR'
#     'STAR'
#     'DIVOP'
#     'MOD'
#     'LSHIFT'
#     'RSHIFT'
#     'NEGATE'
#     'func_main'
#     'f_globals'
#     'const_var_struct'
#     'const_dec'
#     'var_dec'
#     'data_declarations'
#     'data_type'
#     'arg_list'
#     'implement'
#     'funct_list'
#     'pother_oper_def'
#     'pactions'
#     'data_declaration'
#     'ptest_elsif'
#     'pusing_ref'
#     'pcase_val'
#     'pcase_def'
#     'name_ref'
# }









