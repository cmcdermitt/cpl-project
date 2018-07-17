terminal_types = ['ICON', 'FCON', 'HCON', 'IDENTIFIER'] #COMPLETE LATER

class Node:

    def __init__ (self, in_type = 'nonterminal'):
        self.type = in_type
        self.children = []

    #returns the first child node with type = in_type
    def getChildOfType(self, in_type):
        for i, child in enumerate(self.children):
            if isinstance(child, Node):
                if child.type == in_type:
                    return child
        return [] #if the for loop completes without finding a child

    #returns all child nodes with type = in_type
    def getChildrenOfType(self, in_type):
        targets = []
        for i, child in enumerate(self.children):
            if child.type == in_type:
                targets.append(child)
        return targets

