class Variable:
    def __init__(self, var_type, var_value, var_is_const, var_is_global):
        self.type = var_type
        self.value = var_value
        self.is_const = var_is_const
        self.is_global = var_is_global
        
    def __str__(self):
        return 'Variable type: {} value: {} is_const: {} is_global: {}'.format(self.type, self.value, self.is_const, self.is_global)


class VarTable:
    def __init__(self):
        self.variables = {}

    def isDeclared(self, var):
        if var in self.variables.keys():
            return True
        else:
            return False

    def declare(self, var, var_type, is_global = False, is_const = False, value = None):
        if var in self.variables.keys():
            print("Error in declare(): variable {} has already been declared".format(var))
            exit()
        else:
            self.variables[var] = Variable(var_type, value, is_global, is_const)

    def assign(self, var, value):
        if var not in self.variables.keys():
            print("Error in assign(): Undeclared variable {} cannot be assigned a value".format(var))
            exit()
        else:
            self.variables[var].value = value

    def getValue(self, var, pos = 0):
        if var not in self.variables.keys():
            print('Error in get(): variable {} has not been declared'.format(var))
        elif (self.variables[var].value == None):
            print('Error in get(): variable {} has not been assigned a value'.format(var))
        else: 
            var = self.variables[var].value
            if isinstance(var, list): # value will be a list if a variable is declared as an array
                if isinstance(pos, list): # checking that optional param pos was passed in as list
                    if len(pos) == var[0]: # Make sure that the number of [] is appropriate I.E. a 2 dimensional array needs to be accessed with [][]
                        index = 1
                        for x in range(0, pos):
                            if pos[x] < var[1][x]: # Make sure that each index does not go over bounds
                                index = index * pos[x + 1]  # Calculate index as if it is in grid starting with index 1
                        index = index - 1 # Subtract 1 to get 0 based position
                        return var[2][index]
            else:
                return var # For non arrays


    def getType(self, var):
        if var not in self.variables.keys():
            print('Error in get(): variable {} has not been declared'.format(var))
        else:
            return self.variables[var].type

    def __str__(self):
        return str(self.variables)

