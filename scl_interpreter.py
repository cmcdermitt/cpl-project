import scl_var_table

# declare globals
global_vars = scl_var_table.VarTable()
main_vars = scl_var_table.VarTable()
isConst = False
currentTable = None
breakCalled = False


def error(msg, location = ''):
    if location == '':
        print ('Interpreter error: {}'.format(msg))
    else:
        print('Interpreter error: {} in {}'.format(msg, location))
    exit()

def lookup(var_name, arr_pos = 0):
    global global_vars
    global currentTable
    
    if var_name[0] == '\"':
        return var_name

    if currentTable is not None:
        if currentTable.isDeclared(var_name):
            return currentTable.getValue(var_name, arr_pos)
        if global_vars.isDeclared(var_name):
            return global_vars.getValue(var_name, arr_pos)
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
    elif global_vars.isDeclared(var_name):
        return global_vars.getType(var_name, arr_pos)
    else:
        error('variable {} is undeclared and cannnot be looked up'.format(var_name), 'lookupType')

#declare a variable
def declare(name, var_type):
    global currentTable
    global isConst
    currentTable.declare(name, var_type, isConst)

#assign a variable a value
def assign(name, value):
    global currentTable
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
# Type program
# Children: func_main, f_globals, implement
def program(node):
    processNode(node.children[0])
    processNode(node.children[1])
    processNode(node.children[2])

# Expected Structure:
# Type func_main
# Children: none
def func_main(node):
    #func_main should already be verified by the parser and does not do anything
    return

# Expected Structure:
# Type f_globals
# Children: const_dec, var_dec
def f_f_globals(node):
    global currentTable
    global global_vars
    currentTable = global_vars # switch to global scope
    processNode(node.children[0])
    currentTable = main_vars #switch to main function scope

# Expected structure:
# Type: const_dec
# Children: data_declarations or no children
def f_const_dec(node):
    global isConst
    if node.children: #if node.children is not empty
        isConst = True #set flag marking descendent variables as const
        processNode(node.children[0])
        isConst = False #unset flag

# Expected Structure:
# Type var_dec
# Children: data_declarations
def f_var_dec(node):
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
    val = node.children[0] # name of variable
    arrayness = processNode(node.children[1]) # Size of variable (if it is an array or not) NOTE: Lookup will need to be changed to support this
    data_type = processNode(node.children[2]) # Data type of variable; currently no type checking
    declare(val, data_type) # Append variable to proper table
    

# Expected Structure:
# Type array_dec
# Children: plist_const, popt_array_val  
def f_parray_dec(node):
    #size = processNode(node.children[0]) # Get size of array from plist_const
    # contents = processNode(node.children[1]) # Get contents of array from popt_array_val
    # if len(contents) <= len(size): # Fill array
    #     for count in range(0, len(contents)):
    #         size[count] = contents[count]
    # else:
    #     error('parameters is too big for plist')
    # return size
    return

# STRUCTURE
# Type f_plist_const
# Children: IDs
def f_plist_const(node):
    dimensions = [] # All of the elements in the array
    total_num = 1 # Initial size
    dimension_lim = []
    for x in range(len(node.children)):
        c_id = node.children[x]
        if isinstance(c_id, str):
            c_id = lookup(c_id)
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
    return node.value

# Expected Structure:
# Type: pcase_val
# Children: expr, pactions {expr, pactions}
# Parameters: identifier tuple with type and value, and pcase_val node
# Returns: pactions result for the evaluated expr
def f_pcase_val(identifier, node):
    global breakCalled
    # Value of identifier parameter will be our case to check against
    caseCheck = identifier
    # Set empty placeholder for returning if no case executes
    pactionsResult = "Empty"
    # iterate through node expression children only
    # evaluate pactions call associated with index
    for i in range(0, len(node.children), 2):
        exprResult = processNode(node.children[i])
        # Check identifier case against expression value
        if exprResult == caseCheck:
            pactionsResult = processNode(node.children[i+1])
            node = pactionsResult
            if breakCalled:
                return node
    node = pactionsResult
    return node

# Expected structure
# Type: pcase_def
# Children: pactions
# Returns: default pactions result
def f_pcase_def(node):
    node = processNode(node)
    return node

# Expected Structure
# Type: pactions
# Children: action_def { action_def }
def pactions(node):
    for action in node.children:
        processNode(action)

# Begin action_def functions
# Expected Structure
# Type: SET
# Children: name_ref, expr
def f_set(node):
    # Get node type for sentence output
    nodeType = node.type
    # Get identifier tuple
    identifier = processNode(node.children[0])
    exprValue = processNode(node.children[1])
    # Set identifier equal to exprValue
    main_vars.assign(identifier, exprValue)
    return node

# Expected Structure:
# Type: INPUT
# Children: IDENTIFIER
def f_input(node):
    global global_vars
    global main_vars
    # Get input
    input_val = input('Enter input:')
    # Add identifier to variable table
    assign(processNode(node.children[0]), input_val)
    # output results
    print('Variable ' + node.children[0] + ' was assigned')
    # Return node to processNode
    return node

# Expected Structure:
# Type: DISPLAY or DISPLAYN
# Children: IDENTIFIER
def f_display(node):
    #print the value of the IDENTIFIER's variable
    print(lookup(processNode(node.children[0])))
    return node

# Expected Structure:
# Type: INCREMENT
# Children: name_ref => IDENTIFIER
def f_increment(node):
    # Get IDENTIFIER variable
    var = processNode(node.children[0])
    # Get value
    val = main_vars.getValue(var)
    # Increment and assign
    val = val + 1
    main_vars.assign(var, val)
    return node

# Expected Structure:
# Type: DECREMENT
# Children: name_ref => IDENTIFIER
def f_decrement(node):
    # Get IDENTIFIER variable
    var = processNode(node.children[0])
    # Get value
    val = main_vars.getValue(var)
    # Decrement and assign
    val = val - 1
    main_vars.assign(var.value, val)
    return node

# Expected Structure:
# Type: IFELSE
# Children: pcondition, pactions, ptest_elsif, {pactions}
def f_ifelse(node):
    conditional = processNode(node.children[0])
    tempNode = node
    if conditional == True:
        node = processNode(tempNode.children[1])
        return node
    else:
        tempNode = processNode(tempNode.children[2])
    if tempNode == "Empty":
        tempNode = processNode(tempNode.children[3])
    node = tempNode
    return node

# Expected Structure:
# Type: ptest_elsif
# Children: pcondition, pactions
def f_ptest_elsif(node):
    # Temporary return value in case no test evaluates
    pactionsResult = "Empty"
    for i in range(0, len(node.children), 2):
        cond = processNode(node.children[i])
        if cond == True:
            pactionsResult = processNode(node.children[i + 1])
            node = pactionsResult
            return pactionsResult
    node = pactionsResult
    return pactionsResult

# Expected Structure:
# Type: FOR
# Children: name_ref, expr, ( TO | DOWNTO ), expr, pactions
def f_for(node):
    global breakCalled
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
# Type: CASE
# Children: namer_ref, pcase_val, pcase_def
def f_case(node):
    # Get IDENTIFIER from name_ref
    nodeId = processNode(node.children[0])
    tempNode = node
    tempNode = f_pcase_val(nodeId, tempNode.children[1])
    if tempNode == "Empty":
        tempNode = f_pcase_def(tempNode.children[2])
    node = tempNode
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
    # Get nodeType for sentence output
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
    caseCheck = identifier[1]
    # Set empty placeholder for returning if no case executes
    pactionResult = "Empty"
    # iterate through node expression children only
    # evaluate pactions call associated with index
    for i in range(0, len(node.children), 2):
        exprResult = processNode(node.children[i])
        # Check identifier case against expression value
        if exprResult == caseCheck:
            pactionsResult = processNode(node.children[i+1])
            if breakCalled:
                return pactionsResult
    return pactionsResult

# Expected structure
# Type: pcase_def
# Children: pactions
# Returns: default pactions result
def f_pcase_def(node):
    p = processNode(node)
    return p

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
# Children: pcond1 and pcond 1 or pcond 1 
def f_and(node):
    #get children: process if nodes, lookup if strings, then do operation on results
    arg1 = processNode(node.children[0])
    if isinstance(arg1, str):
        arg1 = lookup(arg1)
    if len(node.children) > 1:
        arg2 = processNode(node.children[1])
        if isinstance(arg2, str):
            arg2 = lookup(arg2)
        return arg1 and arg2

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

# Math functions (descending from expr)

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

# numeric constant functions
def f_icon(node):
    return int(node.value)

def f_hcon(node):
    string = node.value
    string = string[:1] + 'x' + string[1:len(string) - 1] #adds x to 0x prefix and strips h suffix
    return int(node.value, 16)

def f_fcon(node):
    return float(node.value)

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
    'PROGRAM' : program,
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
    'FORLOOP' : f_for,
    'WHILELOOP' : f_while,
    'CASE' : f_case,
    'REPEATLOOP' : f_repeat,
    'pcase_val' : f_pcase_val,
    'pcase_def' : f_pcase_def,
    'name_ref' : f_name_ref,
    'pactions' : f_pactions,
    'ptest_elsif' : f_ptest_elsif
}

#     'func_main'
#     'implement'
#     'funct_list'
#     'pother_oper_def'

#for functions:
#     'arg_list'
#     'CALL'
# }









