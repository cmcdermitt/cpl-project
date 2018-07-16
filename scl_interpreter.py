globals = {}

# Then we add all of the global variablse to the globals dictionary
# Then we execute the main function. <- done in implement
def interpret(node):
    global globals
    current = node.getChildOfType('Global')
    if(current == False):
        print("no")

def rglobal(lex_tree):
    dict = {}
    #if lex_tree[2][0] == 'const_dec':


#def rdata_declarations(lex_tree, isconst):


# Checks func_main for errors
#def rfunc_main(lex_tree):
    # valid = True
    # for lex in lex_tree:
    #     if isinstance(lex, list):
    #         valid = rfunc_main(lex)
    #         if(not valid):
    #             return valid
    #     elif isinstance(lex, str):
    #         if(len(lex) >= 5):
    #             print(lex[0:4])
    #             if(lex[0 : 4].upper() == 'ERROR'):
    #                 valid = False
    #                 return valid
    # return valid
