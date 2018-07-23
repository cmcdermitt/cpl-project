from copy import deepcopy

class Variable:
    def __init__(self, var_type, var_value, var_is_const):
        self.type = var_type
        self.value = var_value
        self.is_const = var_is_const
        
    def __str__(self):
        if self.value is not None:
            return 'Variable type: {} value: {} is_const: {}'.format(self.type, self.value, self.is_const)
        else:
            return 'Variable type: {} value: None is_const: {}'.format(self.type, self.is_const)


class VarTable:
    def __init__(self):
        self.variables = {}

    def isDeclared(self, var):
        if var in self.variables.keys():
            return True
        else:
            return False

    def declare(self, var, var_type, is_const = False, value = None):
        if var in self.variables.keys():
            print("Error in declare(): variable {} has already been declared".format(var))
            exit()
        else:
            self.variables[var] = Variable(var_type, value, is_const)

    def arrayA(self, var, value, indices):
        array = self.variables[var].value
        for x in range(0,len(indices) -1):
            array = array[indices[x]]
        if isinstance(array[indices[len(indices) - 1]], list):
            print("Error in array assignment; not enough indices")
            exit()
        array[indices[len(indices) - 1]] = value 
    
    def assignWholeArray(self, varName, value):
        if  isinstance(value, list):
            self.variables[varName] = deepcopy(value)
        else:
            print("Error: you can only assign lists as arrays.")
            exit()

    def getWholeArray(self, varName):
        if isinstance(self.variables[varName], list):
            return deepcopy(self.variables[varName])
        else:
            print('Error: you can only get an array if there\'s an array to get')
            exit()


    def assign(self, var, value, indices = []):
        if var not in self.variables.keys():
            print("Error in assign(): Undeclared variable {} cannot be assigned a value".format(var))
            exit()
        else:
            if type(value) == int and (self.variables[var].type == 'INTEGER' or self.variables[var].type == 'LONG' or self.variables[var].type == 'SHORT'):
                if not indices:
                    self.variables[var].value = value
                else:
                    self.arrayA(var, value, indices)
            elif type(value) == str and (self.variables[var].type == 'TSTRING' or self.variables[var].type == 'CHAR'):
                if not indices:
                    self.variables[var].value = value
                else:
                    self.arrayA(var, value, indices)
            elif type(value) == float and (self.variables[var].type == 'REAL' or self.variables[var].type == 'DOUBLE'):
                if not indices == 0:
                    self.variables[var].value = value
                else:
                    self.arrayA(var, value, indices)
            elif type(value) == bool and self.variables[var].type == 'TBOOL':
                if not indices == 0:
                    self.variables[var].value = value
                else:
                    self.arrayA(var, value, indices)
            else:
                print('Error in assign(): {} variable {} cannot be assigned a {}'.format(self.variables[var].type, self.variables[var].value, type(value)))
                exit()
            
    def getValue(self, var, pos = []):
        if var not in self.variables.keys():
            print('Error in getValue(): variable {} has not been declared'.format(var))
            exit()
        elif (self.variables[var].value == None):
            print('Error in getValue(): variable {} has not been assigned a value'.format(var))
            exit()
        else: 
            var_value = self.variables[var].value
            #return var
            if isinstance(var_value, list): # value will be a list if a variable is declared as an array
                if isinstance(pos, list): # checking that optional param pos was passed in as list
                    currList = var_value
                    for i, x in enumerate(pos):
                        if i < len(pos) - 1:
                            if x >= 0 and x < len(currList[x]):
                                currList = currList[x] #set the current list to the list stored at each position
                            else:
                                print('Error in getValue(): array index {} out of bounds'.format(pos))
                        else:
                            currList = currList[x]

                    if currList is None:
                        print('Error in getValue(): variable {} at {} has not been assigned a value'.format(var, pos))
                        exit()

                    if isinstance(currList, list):
                        print('Error in getValue(): not enough indices for {}'.format(var))
                        exit()

                    return currList
                else:
                    print('Error in getValue(): array {} has no indices'.format(var))
                    exit()
            else:
                return var_value # For non arrays

    # Gets dimensions of array
    # If the variable is not an array, None is returned
    # Otherwise, the dimensions are returned in a list
    def getSize(self, varName):
        indices = []
        varActual = self.variables[varName]
        if not isinstance(varActual, list):
            return None
        else:
            while isinstance(varActual, list):
                indices.append(len(varActual))
                varActual = varActual[0]
            return indices
            


    def getType(self, var, pos = []):
        if var not in self.variables.keys():
            print('Error in get(): variable {} has not been declared'.format(var))
        else:
            return self.variables[var].type

    def __str__(self):
        out = ''
        for name in self.variables:
            out = out + 'Name: {} {}\n'.format(name, self.variables[name])
        return out

    def dump(self):
        print(self.variables)