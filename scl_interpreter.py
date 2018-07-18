# Then we add all of the global variables to the globals dictionary
import scl_var_table
# Then we execute the main function. <- done in implement
interpreterDict = {
    'INPUT': input
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
global_vars = scl_var_table.VarTable()

def error(msg, location = ''):
    if location == '':
        print ('Interpreter error: {}'.format(msg))
    else:
        print('Interpreter error: {} in {}'.format(msg, location))
    exit()

def lookup(var_name, local_scope = None):
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
    nodeType = node.type.upper()
    if nodeType in interpreterDict:
        funct = interpreterDict[nodeType]
        node = funct(node)
    return node

# Expected Structure:
# Type: INPUT
# Children: IDENTIFIER
def input(node):
    # Get associated identifier
    nodeValue = node.children
    # Add identifier to variable table
    variables.declare(nodeValue)
    # Node has no children -> IDENTIFIER is just a string
    # Return node to processNode
    return node

def display(node):
    nodeType = node.type
    nodeValue = node.children

def plus(node):
    for child in node.children:
        if child is instanceof Node:
            child = processNode()
        if child is instanceof str:
            child = variables.getValue()
        return node.children[0] + node.children[1]

def minus(node):
    for child in node.children:
        if child is instanceof Node:
            processNode()
        return node.children[0] - node.children[1]

def band(node):
    for child in node.children:
        if child is instanceof Node:
            processNode()
        return node.children[0]  node.children[1]












