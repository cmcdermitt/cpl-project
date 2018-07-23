import scl_var_table
import sys
import state_machine
from parser_tree import Node

# declare globals

functionNames = {}
variableStack = [scl_var_table.VarTable()]
isConst = False
breakCalled = False
elseRun = False
returnValue = None
interPrint = ''
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
    global variableStack
    if var_name[0] == '\"':
        return var_name
    if var_name in functionNames:
        var_name = functionNames[var_name]
        return startFunction(var_name, arr_pos)
    if variableStack[-1].isDeclared(var_name):
        return variableStack[-1].getValue(var_name, arr_pos)
    if variableStack[0].isDeclared(var_name):
        return variableStack[0].getValue(var_name, arr_pos)
    else:
        error('variable {} is undeclared and cannnot be looked up'.format(var_name), 'lookup')
    

def lookupType(var_name, arr_pos = 0):
    global variableStack
    if variableStack[-1].isDeclared(var_name):
        return variableStack[-1].getType(var_name, arr_pos)
    if variableStack[0].isDeclared(var_name):
        return variableStack[0].getType(var_name, arr_pos)
    else:
        error('variable {} is undeclared and cannnot be looked up'.format(var_name), 'lookup type')

#declare a variable
def declare(name, var_type, val = None):
    global variableStack
    global isConst
    variableStack[-1].declare(name, var_type, isConst, val) 

#assign a variable a value
def assign(name, value, indices = []):
    global variableStack
    if variableStack[-1] is not None:
        if variableStack[-1].isDeclared(name):
            variableStack[-1].assign(name, value, indices)
        else:
            variableStack[0].assign(name, value, indices)
    else:
        variableStack[-1].assign(name, value, indices)

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
    if node.type == 'name_ref' or node.type == 'func_ref':
        return node.children[0].value
    if node.type == 'IDENTIFIER':
        return node.value
    else:
        error('getName only takes name_ref, func_ref, or IDENTIFIER on the input data.')

def isNumber(value):
    return type(value) == int or type(value) == float

def isInteger(value):
    return type(value) == int

# Replacement for pother_oper_def
# Takes a function and runs it with parameters
def startFunction(func, actual_params):
    global returnValue
    if func.children[0].type == 'IDENTIFIER' or func.children[0].value == 'MAIN':
        iden = func.children[0].value
        #print('BEGIN')
        #ys.stdout.write(iden + 'DESCRIPTION IS ')
    oper_type = processNode(func.children[1])

    # Assign params here -> 
    if (func.children[3].type == 'const_var_struct'): # If the function has variables
        variableStack.append(scl_var_table.VarTable()) # Add new variable stack
        formal_params = processNode(func.children[2])
        assignParams(formal_params, actual_params)
        processNode(func.children[3])
        processNode(func.children[4])
        variableStack.pop() # Pop off stack when the pactions are done
        if func.children[5].value != iden:
            error('ENDFUN with correct function not found')
    else:
        formal_params = processNode(func.children[2])
        assignParams(formal_params, actual_params)
        processNode(func.children[3]) # If there are no variables declared just process pactions
        if func.children[4].value != iden:
            error('ENDFUN with correct function not found')
    #print('Statement recognized: ENDFUN ' + iden)
    temp = returnValue
    # if temp != None:
    #     t = type(temp)
    #     if type(temp) != oper_type:
    #         error('opertype does not return correct type')


    returnValue = None
    return temp

def f_oper_type(node):
    return processNode(node.children[0])



def assignParams(formal_params, actual_params):
    global variableStack
    for count, param in  enumerate(formal_params):
        indices = variableStack[-1].getSize(param)
        if indices == None:
            assign(param, actual_params[count],[])
        else:
            temp_param = actual_params[count]
            for index in indices:
                if isinstance(temp_param, list):
                    if len(temp_param) == index:
                        temp_param = temp_param[0]
                    else:
                        error('List does not have correct length')
                else:
                    error('List does not have enough dimensions')
            variableStack[-1].assignWholeArray(param, actual_params[count])


# Expected Structure:
# Type program
# Children: func_main, f_globals, implement
def f_program(node):
    #process func_main
    processNode(node.children[0])
    #process globals
    processNode(node.children[1])
    #process implement
    processNode(node.children[2])

    #start main function
    if 'MAIN' in functionNames:
        startFunction(functionNames['MAIN'], [])
    else:
        error('Main function not found')

# Expected Structure:
# Type func_main
# Children: none
def f_func_main(node):
    #func_main should already be verified by the parser and does not do anything
    funcName = node.children[0]
    print('Statement recognized: ' + node.statement)
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
    global functionNames
    for child in node.children:
        functionNames[child.children[0].value] = child
    return node

# # Expected Structure:
# # Type: pother_oper_def
# # Children: parameters, [const_var_struct], pactions
# def f_pother_oper_def(node):
#     global returnValue
#     if node.children[0].type == 'IDENTIFIER' or node.children[0].value == 'MAIN':
#         iden = node.children[0].value
#         print('BEGIN')
#         sys.stdout.write(iden + 'DESCRIPTION IS ')
#     processNode(node.children[1])
#     processNode(node.children[2])
#     if (node.children[2].type == 'const_var_struct'):
#         processNode(node.children[3])
#         if node.children[4].value != iden:
#             error('ENDFUN with correct function not found')
#     else:
#         if node.children[3].value != iden:
#             error('ENDFUN with correct function not found')
#     print('Statement recognized: ENDFUN ' + iden)
#     return node

# Expected Structure
# Type: parameters
# Children: [data_declaration, {data_declaration}]
def f_parameters(node):
    param_list = []
    for dec in node.children:
        processNode(dec) #declare the parameters
        param_list.append(getName(dec.children[0])) #add the name of each identifier being declared
    return param_list #return list of parameters to start_function

# Expected Structure:
# Type f_globals
# Children: const_dec, var_dec
def f_f_globals(node):
    print('Statement recognized: GLOBAL DECLARATIONS')
    processNode(node.children[0])
    #variableStack[-1] = main_vars #switch to main function scope uncomment when adding multiple functions

# Expected structure:
# Type: const_dec
# Children: data_declarations or no children
def f_const_dec(node):
    global isConst
    if node.children: #if node.children is not empty
        isConst = True #set flag marking descendent variables as const
        #print('CONSTANTS')
        processNode(node.children[0])
        isConst = False #unset flag

# Expected Structure:
# Type var_dec
# Children: data_declarations
def f_var_dec(node):
    #print('Statement recognized: VARIABLES')
    processNode(node.children[0])

# Expected structure:
# Type: data_declarations
# Children: at least one data_declaration
def f_data_declarations(node):
    for child in node.children:
        processNode(child)

# Expected Structure:
# Type: data_declaration
# Children: identifier, parray_dec, data_type
def f_data_declaration(node):
    array = processNode(node.children[1]) # list
    data_type = processNode(node.children[2]) # Data type of variable
    if array:
        declare(getName(node.children[0]), data_type, array) # Append variable to proper table
    else:
        declare(getName(node.children[0]), data_type) # Append variable to proper table
    #print('Statement recognized: DEFINE ' + node.children[0].value + " OF " + str(data_type))

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
    outList = [processNode(child) for child in node.children]
    return outList

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
        if returnValue == None:
            processNode(action)
        else:
            return returnValue

# Begin action_def functions
# Expected Structure
# Type: SET
# Children: name_ref, expr
def f_set(node):
    global interPrint
    # Get identifier tuple
    identifier = getName(node.children[0])
    exprValue = processNode(node.children[1])
    indices = getIndices(node.children[0])
    assign(identifier, exprValue, indices)
    #print('Statement recognized: SET ' + identifier + ' EQUOP ' + str(exprValue))
    return node

# Expected Structure:
# Type: INPUT
# Children: name_ref
def f_input(node):
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
    assign(getName(node.children[0]), processNode(tempNode), getIndices(node.children[0]))
    # output results
    #print('Statement recognized: INPUT ' + str(getName(node.children[0])))
    # Return node to processNode
    return node

# Expected Structure:
# Type: DISPLAY or DISPLAYN
# Children: name_ref
def f_display(node):
    #print the value of the IDENTIFIER's variable
    # Change actual output after debuging
    pNode = processNode(node.children[0])
    print(pNode)
    #print('Statement recognized: DISPLAY ' + str(pNode))
    return node

# Expected Structure:
# Type: INCREMENT
# Children: name_ref => IDENTIFIER
def f_increment(node):
    # Get IDENTIFIER variable
    var = getName(node.children[0])
    # Get indices
    indices = getIndices(node.children[0])
     # Get value
    val = processNode(node.children[0])
    # Increment and assign
    val = val + 1
    assign(var, val, indices)
    #print('Statement recognized: INCREMENT ' + var)
    return node

# Expected Structure:
# Type: DECREMENT
# Children: name_ref => IDENTIFIER
def f_decrement(node):
    # Get IDENTIFIER variable
    var = getName(node.children[0])
    # Get value
    val = processNode(node.children[0])
    # Get indices
    indices = getIndices(node.children[0])
    # Increment and assign
    val = val - 1
    assign(var, val, indices)
    #print('Statement recognized: DECREMENT ' + var)
    return node

# Expected Structure:
# Type: IFELSE
# Children: pcondition, pactions, ptest_elsif, {pactions}
def f_ifelse(node):
    global elseRun
    #print('Statement recognized: IF ')
    if processNode(node.children[0]):
        #print('THEN  ', end = '')
        processNode(node.children[1])
        return node
    else:
        elseRun = not processNode(node.children[2]) and len(node.children) == 4 # Check if else stmt exists
    if elseRun == True:
        elseRun = False
        #print('ELSE ', end = '')
        processNode(node.children[3])
    #print('ENDIF', end = '')
    return node

# Expected Structure:
# Type: ptest_elsif
# Children: pcondition, pactions
def f_ptest_elsif(node):
    cond = False
    #print('ELSE IF ')
    for i in range(0, len(node.children), 2):
        cond = processNode(node.children[i])
        #print(str(cond) + ' ')
        if cond == True:
            processNode(node.children[i + 1])
    return cond

# Expected Structure:
# Type: FOR
# Children: name_ref, expr, ( TO | DOWNTO ), expr, pactions
def f_for(node):
    global breakCalled
    expr1 = processNode(node.children[1])
    # Determine if direction is TO or DOWNTO
    dir = processNode(node.children[2]).type
    # Get second expr of for loop
    expr2 = processNode(node.children[3])
    # Get indices for potential array
    indices = getIndices(node.children[0])
    # Assign initial value to IDENTIFIER
    #print('Statement recognized: FOR ' + getName(node.children[0]) + ' EQUOP ' + str(expr1) + str(dir) + str(expr2) + 'DO ')
    assign(getName(node.children[0]), expr1, indices)
    # Perform for loop up or down
    var = processNode(node.children[0])
    if not (isInteger(var) and isInteger(expr1) and isInteger(expr2)):
        error('Bad types in for loop')

    if dir == 'TO':
        if var > expr2:
            error('var should be less than expr')
        while var < expr2:
            # Process pactions each time
            processNode(node.children[4])
            var = processNode(node.children[0])
            var += 1
            assign(getName(node.children[0]), var, indices)
            
            
            if breakCalled == True:
                breakCalled = False
                return node
            # Increment and assign
    else:
        while var > expr2:
            if var < expr2: 
                error('var should be greater than expr')
            processNode(node.children[4])    
            var = processNode(node.children[0])
            var -= 1
            assign(getName(node.children[0]), var, indices)
        
           
            if breakCalled == True:
                breakCalled = False
                return node
            # Decrement and assign

    #sys.stdout.write('ENDFOR')
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
    #print('Statement recognized: REPEAT ')
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
    #sys.stdout.write('UNTIL ' + str(cond) + 'ENDREPEAT')
    return node

# Expected Structure:
# Type: WHILE
# Children pcondition, pactions
def f_while(node):
    global breakCalled
    # Get pcondition
    cond = processNode(node.children[0])
    #print('Statement recognized: WHILE CONDITION DO')
    # Start while loop
    while cond:
        p = processNode(node.children[1])
        if breakCalled == True:
            breakCalled = False
            return node
        cond = processNode(node.children[0])
    #sys.stdout.write('ENDWHILE')
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
    #print('Statement recognized: CASE ' + str(nodeId) + ' ')
    successfulCase = f_pcase_val(nodeId, node.children[1])
    if breakCalled == True:
        breakCalled = False
    if(not successfulCase and len(node.children) == 3):
        f_pcase_def(node.children[2])
    #sys.stdout.write('MENDCASE')
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
    if len(node.children) == 1:
        return processNode(node.children[0])
    else:

        # val =  processNode(node.children[0])
        name = node.children[0].value
        indices =  processNode(node.children[1])
        return lookup(name, indices)

# Expected Structure:
# Type: func_ref
# Children: Identifier, arg_list
# Returns: value of evaluated function
def f_func_ref(node):
    func = functionNames[getName(node.children[0])]
    params = processNode(node.children[1])
    return startFunction(func, params)

def getIndices(name_ref):
    if len(name_ref.children) > 1:
        return processNode(name_ref.children[1])
    else:
        return []

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
        #print('MWHEN ' + str(exprResult) + ' COLON ')
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

def f_call(node):
    func = getName(node.children[0])
    if func in functionNames:
        func = functionNames[func]
    else:
        error('Function not in function names')
    params = processNode(node.children[1])
    return startFunction(func, params)

def f_pusing_ref(node):
    return processNode(node.children[0])

def f_return(node):
    global returnValue
    returnValue = processNode(node.children[0])
    return returnValue

# Logic operator functions (descending from pcondition)

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

def f_array_val(node):
    indices = processNode(node.children[0])
    return indices

def f_arg_list(node):
    indices = []
    for child in node.children:
        indices.append(processNode(child))
    return indices


    
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
    'PARAMETERS' : f_parameters,
    'SET' : f_set,
    'FCON' : f_fcon,
    'TSTRING' : f_tstring,
    'LETTER' : f_tstring,
    'STRING' : f_tstring,
    'CHAR' : f_tstring,
    'IDENTIFIER' : f_identifier,
    'ARRAY_VAL' : f_array_val,
    'ARG_LIST' : f_arg_list,
    'RETURN' : f_return,
    'CALL' : f_call,
    'PUSING_REF' : f_pusing_ref,
    'FUNC_REF' : f_func_ref,
    'OPER_TYPE' : f_oper_type
}

#for functions:
#     'arg_list'
#     'CALL'
# }









