class Node:

    def __init__ (self, in_type, in_value = None):
        self.type = in_type
        self.value = in_value
        self.children = []
        self.statement = ''

    #returns the first child node with type = in_type
    def getChildOfType(self, in_type):
        for child in self.children:
            if isinstance(child, Node):
                if child.type == in_type:
                    return child
        return [] #if the for loop completes without finding a child

    #returns all child nodes with type = in_type
    def getChildrenOfType(self, in_type):
        targets = []
        for child in self.children:
            if child.type == in_type:
                targets.append(child)
        return targets

    def __str__(self):
        return 'Node type: {} value: {}'.format(self.type, self.value)

