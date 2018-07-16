terminal_types = ['ICON', 'FCON', 'HCON', 'IDENTIFIER'] #COMPLETE LATER

class Node:

    def __init__ (self, in_val, in_type = 'nonterm'):
        self.value = in_val
        self.type = in_type
        self.children = []


    #returns the child at the given index
    def getChildAt(self, index):
        return self.children[index]

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

    #adds a child to children
    def addChild(self, child):
        self.children.append(child)

    #returns the index of the first child of that type, or -1 if there isn't one.
    def hasChild(self, value):
        for i, child in enumerate(self.children):
            if child.type == value:
                return i
        return -1 #if the for loop completes without finding a child
