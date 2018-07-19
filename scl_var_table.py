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

    def assign(self, var, value):
        if var not in self.variables.keys():
            print("Error in assign(): Undeclared variable {} cannot be assigned a value".format(var))
            exit()
        else:
            self.variables[var].value = value

    def getValue(self, var):
        if var not in self.variables.keys():
            print('Error in get(): variable {} has not been declared'.format(var))
        elif (self.variables[var].value == None):
            print('Error in get(): variable {} has not been assigned a value'.format(var))
        else:
            return self.variables[var].value

    def getType(self, var):
        if var not in self.variables.keys():
            print('Error in get(): variable {} has not been declared'.format(var))
        else:
            return self.variables[var].type

    def __str__(self):
        out = ''
        for name in self.variables:
            out = out + 'Name: {} {}\n'.format(name, self.variables[name])
        return out



