# globals = {}

# Then we add all of the global variablse to the globals dictionary
# Then we execute the main function. <- done in implement
def interpret(node):
    global globals
    globals = rglobal(node.getChildOfType('globals'))

def rglobal(node):
    dict = {}
    if node.hasChild('const_dec'):
        const_node = node.getChildOfType('const_dec')
        const_node = const_node.getChildOfType('data_declarations')
        rdata_declarations(const_node, dict, True)
    if node.hasChild('var_dec'):
        var_node = node.getChildOfType('var_dec')
        var_node = var_node.getChildOfType('data_declarations')
        rdata_declarations(var_node, dict, False)

def rdata_declarations(node, dict, isConst):
    data_decs = node.getChildrenOfType('comp_declare')
    for comp_dec in data_decs:
        data_dec = rdata_declaration(comp_dec)
        dict[data_dec[0]] = [data_dec[1], data_dec[2], isConst]

def rdata_declaration(node):
    data_dec = node.getChildOfType('data_declaration')
    id = data_dec.getChildAt(1)
    type = data_dec.getChildOfType('data_type')
    parray = None
    if data_dec.hasChild('parray_dec'):
        parray = data_dec.getChildOfType('parray_dec')
    return[1,2,3]
