import scl_var_table
import sys
import state_machine
from parser_tree import Node

# declare globals
global_vars = scl_var_table.VarTable()
main_vars = scl_var_table.VarTable()
functionNames = []
isConst = False
currentTable = None
breakCalled = False
elseRun = False

# Main interpreter function
# Name: processNode(node)
# Summary: The processNode function is invoked by the main file after the parser has
#          generated the tree basedpret function is recognize keywords and parsed functions
#          and call corresponding functions based on the value.
#          Each function will receive a subtree containing the nodes from that keyword down,
#          and will set the new starting node after it has finished processing any related nodes
# Return: No output currently
def processNode(node):
    #print('processing {} node {}'.format(node.type, node.value))
    nodeType = node.type.upper()
    if node.type.upper() == 'KEYWORD':
        nodeType = node.value.upper() #for MTRUE and MFALSE
    if nodeType in interpreterDict:
        funct = interpreterDict[nodeType]
        node = funct(node)
    return node

def error(msg, location = ''):
    if location == '':
        print ('Interpreter error: {}'.format(msg))
    else:
        print('Interpreter error: {} in {}'.format(msg, location))
    exit()

def lookup(var_name, arr_pos = []):
    global global_vars
    global currentTable
    
    if var_name[0] == '\"':
        return var_name

    if currentTable is not None:
        if currentTable.isDeclared(var_name):
            return currentTable.getValue(var_name, arr_pos)
        if global_vars.isDeclared(var_name):
            return global_vars.getValue(var_name, arr_pos)
        else:
            error('variable {} is undeclared and cannnot be looked up'.format(var_name), 'lookup')
    elif global_vars.isDeclared(var_name):
        return global_vars.getValue(var_name, arr_pos)
    else:
        error('variable {} is undeclared and cannnot be looked up'.format(var_name), 'lookup')

def lookupType(var_name, arr_pos = 0):
    if currentTable is not None:
        if currentTable.isDeclared(var_name):
            return currentTable.getType(var_name, arr_pos)
        if global_vars.isDeclared(var_name):
            return global_vars.getType(var_name, arr_pos)
        else:
            error('variable {} is undeclared and cannnot be looked up'.format(var_name), 'lookup type')
    elif global_vars.isDeclared(var_name):
        return global_vars.getType(var_name, arr_pos)
    else:
        error('variable {} is undeclared and cannot be looked up'.format(var_name), 'lookupType')

#declare a variable
def declare(name, var_type, val = None):
    global currentTable
    global isConst
    currentTable.declare(name, var_type, isConst, val) 

#assign a variable a value
def assign(name, value):
    global currentTable
    if currentTable is not None:
        if currentTable.isDeclared(name):
            currentTable.assign(name, value)
        else:
            global_vars.assign(name, value)
    else:
        currentTable.assign(name, value)

# Get the type of what's stored in a name_ref ID, or data node
def getType (node):
    if node.type == 'name_ref':
        var =  node.children[0].value #return the type of the ID stored in the name_ref
        return lookupType(var)
    if node.type == 'IDENTIFIER':
        var = node.value
        return lookupType(var) # return the type of the value associated with the variable
    return node.type

# Get the ID value name of a name_ref or identifier node
def getName (node):
    if node.type == 'name_ref':
        return node.children[0].value
    if node.type == 'IDENTIFIER':
        return node.value
    else:
        error('getName only takes name_ref or IDENTIFIER on the input data.')

def isNumber(value):
    return type(value) == int or type(value) == float

def isInteger(value):
    return type(value) == int


# Expected Structure:
# Type program
# Children: func_main, f_globals, implement
def f_program(node):
    processNode(node.children[0])
    processNode(node.children[1])
    processNode(node.children[2])

# Expected Structure:
# Type func_main
# Children: none
def f_func_main(node):
    #func_main should already be verified by the parser and does not do anything
    funcName = node.children[0]
    functionNames.append(funcName)
    print('Statement recognized: FUNCTION ' + str(funcName.value) + ' RETURN MVOID')
    return

# Expected Structure:
# Type: implement
# Children: funct_list
def f_implement(node):
    # Remainder of statement printed by f_funct_list children
    print('Statement recognized: IMPLEMENTATIONS ')
    processNode(node.children[0])
    return node

# Expected Structure
# Type: funct_list
# Children: pother_oper_def, {pother_oper_def}
def f_funct_list(node):
    for child in node.children:
        print('Statement recognized: FUNCTION ')
        processNode(child)
    return node

# Expected Structure:
# Type: pother_oper_def
# Children: parameters, [const_var_struct], pactions
def f_pother_oper_def(node):
    if node.children[0].type == 'IDENTIFIER':
        iden = node.children[0].value
        print('BEGIN')
        sys.stdout.write(iden + 'DESCRIPTION IS ')
    processNode(node.children[1])
    processNode(node.children[2])
    if (node.children[2].type == 'const_var_struct'):
        processNode(node.children[3])
        if node.children[4].value != iden:
            error('ENDFUN with correct function not found')
    else:
        if node.children[3].value != iden:
            error('ENDFUN with correct function not found')
    print('Statement recognized: ENDFUN ' + iden)
    return node

# Expected Structure
# Type: parameters
# Children: [data_declaration, {data_declaration}]
def f_parameters(node):
    for dec in node.children:
        processNode(dec)
    return node

# Expected Structure:
# Type f_globals
# Children: const_dec, var_dec
def f_f_globals(node):
    global currentTable
    global global_vars
    print('Statement recognized: GLOBAL DECLARATIONS')
    currentTable = global_vars # switch to global scope
    processNode(node.children[0])
    #currentTable = main_vars #switch to main function scope uncomment when adding multiple functions

# Expected structure:
# Type: const_dec
# Children: data_declarations or no children
def f_const_dec(node):
    global isConst
    if node.children: #if node.children is not empty
        isConst = True #set flag marking descendent variables as const
        print('CONSTANTS')
        processNode(node.children[0])
        isConst = False #unset flag

# Expected Structure:
# Type var_dec
# Children: data_declarations
def f_var_dec(node):
    print('Statement recognized: VARIABLES')
    processNode(node.children[0])

# Expected structure:
# Type: data_declarations
# Children: at least one data_declaration
def f_data_declarations(node):
    for child in node.children:
        processNode(child)

# Expected Structure:
# Type: data_declaration
# Children: 
def f_data_declaration(node):
    global currentTable # Table to append to
    array = processNode(node.children[1]) # Size of variable (if it is an array or not) NOTE: Lookup will need to be changed to support this
    data_type = processNode(node.children[2]) # Data type of variable; currently no type checking
    if len(array) == 0:
        declare(getName(node.children[0]), data_type) # Append variable to proper table
    else:
        declare(getName(node.children[0]), data_type, array) # Append variable to proper table
    print('Statement recognized: DEFINE ' + node.children[0].value + " OF " + str(data_type))

# Expected Structure:
# Type array_dec
# Children: plist_const 
def f_parray_dec(node):
    array = []
    if(len(node.children) > 0):
        array = makeMultiList(processNode(node.children[0]))
    return array

def makeMultiList (arg1, pos = 0):
    if (pos < len(arg1) - 1):
        return [makeMultiList(arg1, pos + 1) for i in range(0, arg1[pos])] #call again if there are more dimensions
    else:
        return [None for i in range (0, arg1[pos])] #fill with none
            


        


# STRUCTURE
# Type f_plist_const
# Children: IDs
def f_plist_const(node):
    dimensions = [] # All of the elements in the array
    total_num = 1 # Initial size
    dimension_lim = []
    for x in range(len(node.children)):
        c_id = processNode(node.children[x])
        dimension_lim.append(c_id)
        total_num = c_id * total_num # Find the total number of locations in the array by multiplying all the dimensions
    for a in range (0,total_num):
        dimensions.append(0) # Fill dimensions with the number of items (when accessed, the dimension numbers will be multiplied together to reach the index)
    if len(dimensions) == 0:
        dimensions = 0
        return dimensions
    return [len(node.children),dimension_lim,dimensions] # The length of the children is used to see how many dimensions there are. I.E. array int[5][6]; array[24] would be wrong

# STRUCTURE
# Type popt_array_val
# Children: Expressions
def f_popt_array_val(node):
    expressions = []
    temp = 0
    for expr in node.children: # evaluate all expressions
        temp = processNode(expr)
        expressions.append(temp) # add it to list
    return expressions

# Expected structure:
# Type: const_var_struct
# Children: const_dec var_dec
def f_const_var_struct(node):
    processNode(node.children[0])
    processNode(node.children[1])

# Expected structure:
# Type: data_type
# Children: keyword
def f_data_type(node):
    #sys.stdout.write(" " + node.value)
    return node.value

# Expected Structure
# Type: pactions
# Children: action_def { action_def }
def f_pactions(node):
    for action in node.children:
        processNode(action)

# Begin action_def functions
# Expected Structure
# Type: SET
# Children: name_ref, expr
def f_set(node):
    # Get identifier tuple
    identifier = getName(node.children[0])
    exprValue = processNode(node.children[1])
    # Set identifier equal to exprValue
    assign(identifier, exprValue)
    print('Statement recognized: SET ' + identifier + ' EQUOP ' + str(exprValue))
    return node

# Expected Structure:
# Type: INPUT
# Children: IDENTIFIER
def f_input(node):
    global global_vars
    global main_vars
    # Get input
    input_val = input('Enter input:')
    #Run state_machine.processLine to get the first token in the line
    input_val = state_machine.processLine(input_val)[0] #ignore any tokens past the first
    if input_val[1] == 'IDENTIFIER':
        input_val[1] = 'TSTRING' #since the scanner treats arbitrary unquoted text as identifiers, convert it to string
    #put the token in a node so we can use the functions we already have to get its value
    tempNode = Node(input_val[1], input_val[0])
    

    # Add identifier to variable table
    assign(getName(node.children[0]), processNode(tempNode))
    # output results
    print('Statement recognized: INPUT ' + str(node.children[0].value))
    # Return node to processNode
    return node

# Expected Structure:
# Type: DISPLAY or DISPLAYN
# Children: IDENTIFIER
def f_display(node):
    #print the value of the IDENTIFIER's variable
    # Change actual output after debuging
    pNode = processNode(node.children[0])
    print(pNode)
    print('Statement recognized: DISPLAY ' + str(pNode))
    return node

# Expected Structure:
# Type: INCREMENT
# Children: name_ref => IDENTIFIER
def f_increment(node):
    # Get IDENTIFIER variable
    var = getName(node.children[0])
    # Get value
    val = lookup(var)
    # Increment and assign
    val = val + 1
    assign(var, val)
    print('Statement recognized: INCREMENT ' + var)
    return node

# Expected Structure:
# Type: DECREMENT
# Children: name_ref => IDENTIFIER
def f_decrement(node):
    # Get IDENTIFIER variable
    var = getName(node.children[0])
    # Get value
    val = lookup(var)
    # Increment and assign
    print(val)
    print(var)
    val = val - 1
    assign(var, val)
    print('Statement recognized: DECREMENT ' + var)
    return node

# Expected Structure:
# Type: IFELSE
# Children: pcondition, pactions, ptest_elsif, {pactions}
def f_ifelse(node):
    global elseRun
    print('Statement recognized: IF ')
    if processNode(node.children[0]):
        print('THEN  ', end = '')
        processNode(node.children[1])
        return node
    else:
        elseRun = not processNode(node.children[2]) and len(node.children) == 4 # Check if else stmt exists
    if elseRun == True:
        elseRun = False
        print('ELSE ', end = '')
        processNode(node.children[3])
    print('ENDIF', end = '')
    return node

# Expected Structure:
# Type: ptest_elsif
# Children: pcondition, pactions
def f_ptest_elsif(node):
    cond = False
    print('ELSE IF ')
    for i in range(0, len(node.children), 2):
        cond = processNode(node.children[i])
        print(str(cond) + ' ')
        if cond == True:
            processNode(node.children[i + 1])
    return cond

# Expected Structure:
# Type: FOR
# Children: name_ref, expr, ( TO | DOWNTO ), expr, pactions
def f_for(node):
    global breakCalled
    global currentTable
    expr1 = processNode(node.children[1])
    # Determine if direction is TO or DOWNTO
    dir = processNode(node.children[2]).type
    # Get second expr of for loop
    expr2 = processNode(node.children[3])
    # Assign initial value to IDENTIFIER
    print('Statement recognized: FOR ' + getName(node.children[0]) + ' EQUOP ' + str(expr1) + str(dir) + str(expr2) + 'DO ')
    currentTable.assign(getName(node.children[0]), expr1)
    # Perform for loop up or down
    var = processNode(node.children[0])
    if not (isInteger(var) and isInteger(expr1) and isInteger(expr2)):
        error('Bad types in for loop')

    if dir == 'TO':
        if var > expr2:
            error('var should be less than expr')
        while var < expr2:
            # Process pactions each time
            var += 1
            currentTable.assign(getName(node.children[0]), var)
            processNode(node.children[4])
            if breakCalled == True:
                breakCalled = False
                return node
            # Increment and assign
    else:
        while var > expr2:
            if var < expr2: 
                error('var should be greater than expr')
            var -= 1
            currentTable.assign(getName(node.children[0]), var)
            processNode(node.children[4])
            if breakCalled == True:
                breakCalled = False
                return node
            # Decrement and assign

    sys.stdout.write('ENDFOR')
    return node

# Expected Structure:
# Type: REPEAT
# Children pactions, pcondition
def f_repeat(node):
    global breakCalled
    # Emulate a do-while by executing pactions once,
    # and repeating in while loop until conditional is false
    #
    # Perform initial pactions statement
    print('Statement recognized: REPEAT ')
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
    sys.stdout.write('UNTIL ' + str(cond) + 'ENDREPEAT')
    return node

# Expected Structure:
# Type: WHILE
# Children pcondition, pactions
def f_while(node):
    global breakCalled
    # Get pcondition
    cond = processNode(node.children[0])
    print('Statement recognized: WHILE CONDITION DO')
    # Start while loop
    while cond:
        p = processNode(node.children[1])
        if breakCalled == True:
            breakCalled = False
            return node
        cond = processNode(node.children[0])
    sys.stdout.write('ENDWHILE')
    return node

# Expected Structure:
# Type: CASE
# Children: name_ref, pcase_val, pcase_def
def f_case(node):
    global breakCalled
    # Get IDENTIFIER from name_ref
    nodeId = processNode(node.children[0])
    if not isInteger(nodeId):
        error('Type error: case ID must be an integer')
    print('Statement recognized: CASE ' + str(nodeId) + ' ')
    successfulCase = f_pcase_val(nodeId, node.children[1])
    if breakCalled == True:
        breakCalled = False
    if(not successfulCase and len(node.children) == 3):
        f_pcase_def(node.children[2])
    sys.stdout.write('MENDCASE')
    return node

# Expected Structure:
# Type: MBREAK
# Children: none
def f_mbreak(node):
    global breakCalled
    breakCalled = True
    return node

# Expected Structure:
# Type: MEXIT
# Children: none
def f_mexit(node):
    exit()

# Expected Structure:
# Type: name_ref
# Children: Identifier
# Returns: Type and value of IDENTIFIER in tuple
def f_name_ref(node):
    return processNode(node.children[0])

# Expected Structure:
# Type: pcase_val
# Children: expr, pactions {expr, pactions}
# Parameters: identifier tuple with type and value, and pcase_val node
# Returns: pactions result for the evaluated expr
def f_pcase_val(node, identifier = ()):
    global breakCalled
    if identifier == ():
        error('pcase_val needs an identifier', 'pcase_val')
    # Value of identifier parameter will be our case to check against
    caseCheck = lookup(node.value)
    if isInteger(caseCheck) and isInteger(identifier[0]):
        error('All cases must be integers')

    caseRan = False
    # iterate through node expression children only
    # evaluate pactions call associated with index
    for i in range(0, len(identifier.children), 2):
        exprResult = processNode(identifier.children[i])
        print('MWHEN ' + str(exprResult) + ' COLON ')
        # Check identifier case against expression value
        if exprResult == caseCheck:
            caseRan = True
            processNode(identifier.children[i+1])
            if breakCalled:
                breakCalled = False
                return caseRan
    return caseRan

# Expected structure
# Type: pcase_def
# Children: pactions
# Returns: default pactions result
def f_pcase_def(node):
    if len(node.children) == 1:
        p = processNode(node.children[0])
    return node

# Expected Structure:
# Type: CALL
# Children: name_ref => IDENTIFIER
# def f_call(node):
#     # Get node type
#     nodeType = node.type
#     for child in node.children:
#         if isinstance(child, node):
#             processNode(child)
#         else:
#             callValue = main_vars.getValue(node.children[0])
#             print(callValue)
#     return node
# Logic functions (descending from pcondition)

# Type AND
# Children: pcond1 and pcond 1
def f_and(node):
    #get children: process if nodes, lookup if strings, then do operation on results
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if type(arg1) == bool and type(arg2) == bool:
        print (' {} AND {} '.format(arg1, arg2))
        return arg1 and arg2        
    else:
        error('Type error: {} and {} are not compatible for AND'.format(type(arg1), type(arg2)))

# Expected Structure:
# Type OR
# Children: pcond1 and pcond 1
def f_or(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if type(arg1) == bool and type(arg2) == bool:
        print (' {} OR {} '.format(arg1, arg2))
        return arg1 and arg2
    else:
        error('Type error: {} and {} are not compatible for OR'.format(type(arg1), type(arg2)))

#Expected Structure
#TYPE NOT
#Children: Expr
def f_not(node):
    arg1 = processNode(node.children[0])
    if isinstance(arg1, bool):
        return arg1
    else:
        error('Type error: {} not valid for NOT'.format(type(arg1)))

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
    #get the values of both children, then compare them
    return processNode(node.children[0]) == processNode(node.children[1])

# Expected Structure:
# Type greater_than
# Children: expr, expr
def f_greater_than(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if type(arg1) != type(arg2) or not isNumber(arg1) or not isNumber(arg2):
        error('Type error: {} and {} are not compatible for GREATER THAN'.format(type(arg1), type(arg2)))
    return arg1 > arg2

# Expected Structure:
# Type less_than
# Children: expr, expr
def f_less_than(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if type(arg1) != type(arg2) or not isNumber(arg1) or not isNumber(arg2):
        error('Type error: {} and {} are not compatible for LESS THAN'.format(type(arg1), type(arg2)))
    return arg1 < arg2

# Expected Structure:
# Type greater_or_equal
# Children: expr, expr
def f_greater_or_equal(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if type(arg1) != type(arg2) or not isNumber(arg1) or not isNumber(arg2):
        error('Type error: {} and {} are not compatible for GREATER OR EQUAL'.format(type(arg1), type(arg2)))
    return arg1 >= arg2

# Expected Structure:
# Type less_or_equal
# Children: expr, expr

def f_less_or_equal(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if type(arg1) != type(arg2) or not isNumber(arg1) or not isNumber(arg2):
        error('Type error: {} and {} are not compatible for LESS OR EQUAL'.format(type(arg1), type(arg2)))
    return arg1 <= arg2

# Math functions (descending from expr)

def f_plus(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if (isNumber(arg1) or type(arg1) == str) and type(arg1) == type(arg2):
        return arg1 + arg2
    else:
        error('Type error: {} and {} are not compatible for PLUS'.format(type(arg1), type(arg2)))


def f_minus(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isNumber(arg1) and type(arg1) == type(arg2):
        return arg1 - arg2
    else:
        error('Type error: {} and {} are not compatible for MINUS'.format(type(arg1), type(arg2)))

def f_band(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isInteger(arg1) and isInteger(arg2):
        return arg1 & arg2
    else:
        error('Type error: operands for BAND must be integers, not  {} and {}'.format(type(arg1), type(arg2)))

def f_bor(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isInteger(arg1) and isInteger(arg2):
        return arg1 | arg2
    else:
        error('Type error: operands for BOR must be integers, not  {} and {}'.format(type(arg1), type(arg2)))

def f_bxor(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isInteger(arg1) and isInteger(arg2):
        return arg1 ^ arg2
    else:
        error('Type error: operands for BXOR must be integers, not  {} and {}'.format(type(arg1), type(arg2)))

def f_star(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isNumber(arg1) and type(arg1) == type(arg2):
        return arg1 * arg2
    else:
        error('Type error: {} and {} are not compatible for STAR'.format(type(arg1), type(arg2)))

def f_divop(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isInteger(arg1) and isInteger(arg2):
        return arg1 // arg2
    elif isNumber(arg1) and type(arg1) == type(arg2):
        return arg1 / arg2
    else:
        error('Type error: {} and {} are not compatible for DIVOP'.format(type(arg1), type(arg2)))

def f_mod(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isInteger(arg1) and isInteger(arg2):
        return arg1 % arg2
    else:
        error('Type error: Arguments for MOD must be integers, not {} and {}'.format(type(arg1), type(arg2)))

def f_lshift(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isInteger(arg1) and isInteger(arg2):
        return arg1 << arg2
    else:
        error('Type error: Arguments for LSHIFT must be integers, not {} and {}'.format(type(arg1), type(arg2)))

def f_rshift(node):
    arg1 = processNode(node.children[0])
    arg2 = processNode(node.children[1])
    if isInteger(arg1) and isInteger(arg2):
        return arg1 >> arg2
    else:
        error('Type error: Arguments for MOD must be integers, not {} and {}'.format(type(arg1), type(arg2)))

def f_negate(node):
    arg = processNode(node.children[0])
    if isNumber(arg):
        return -arg
    else:
        error('Type error: Argument for NEGATE must be a number, not {}'.format(type(arg)))

# numeric constant functions
def f_icon(node):
    return int(node.value)

def f_tstring(node):
    return str(node.value)

def f_hcon(node):
    string = node.value
    string = string[:1] + 'x' + string[1:len(string) - 1] #adds x to 0x prefix and strips h suffix
    return int(node.value, 16)

def f_fcon(node):
    return float(node.value)

def f_identifier(node):
    return lookup(node.value)

#dictionary associating node types with functions
interpreterDict = {
    'INPUT': f_input,
    'DISPLAY' : f_display,
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
    'ICON' : f_icon,
    'MBREAK' : f_mbreak,
    'MEXIT' : f_mexit,
    'F_GLOBALS' : f_f_globals,
    'CONST_VAR_STRUCT' : f_const_var_struct,
    'PROGRAM' : f_program,
    'CONST_DEC' : f_const_dec,
    'VAR_DEC' : f_var_dec,
    'DATA_DECLARATIONS' : f_data_declarations,
    'DATA_DECLARATION' : f_data_declaration,
    'PARRAY_DEC' : f_parray_dec,
    'PLIST_CONST' : f_plist_const,
    'POPT_ARRAY_VAL' : f_popt_array_val,
    'DATA_TYPE' : f_data_type,
    'INCREMENT' : f_increment,
    'DECREMENT' : f_decrement,
    'IFELSE' : f_ifelse,
    'FOR' : f_for,
    'WHILE' : f_while,
    'CASE' : f_case,
    'REPEAT' : f_repeat,
    'PCASE_VAL' : f_pcase_val,
    'PCASE_DEF' : f_pcase_def,
    'NAME_REF' : f_name_ref,
    'PACTIONS' : f_pactions,
    'PTEST_ELSIF' : f_ptest_elsif,
    'IMPLEMENT' : f_implement,
    'FUNC_MAIN' : f_func_main,
    'FUNCT_LIST' : f_funct_list,
    'POTHER_OPER_DEF' : f_pother_oper_def,
    'PARAMETERS' : f_parameters,
    'SET' : f_set,
    'FCON' : f_fcon,
    'TSTRING' : f_tstring,
    'LETTER' : f_tstring,
    'STRING' : f_tstring,
    'CHAR' : f_tstring,
    'IDENTIFIER' : f_identifier 
}

#for functions:
#     'arg_list'
#     'CALL'
# }









