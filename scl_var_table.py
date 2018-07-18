class Variable:
    def __init__(self, var_type, var_value, var_is_const, var_is_global):
        self.type = var_type
        self.value = var_value
        self.is_const = var_is_const
        self.is_global = is_global


class VarTable:

    def __init__(self):
        variables = {}

    def declare(self, var, var_type, is_global = False, is_const = False, value = None):
        if var in self.variables.keys():
            print("Error in declare(): variable {} has already been declared".format(var))
            exit()
        else:
            self.variables[var] = Variable(var_type, value, var_type, is_global, is_const)

    def assign(self, var, value):
        if var not in self.variables.keys():
            print("Error in assign(): Undeclared variable {} cannot be assigned a value".format(var))
            exit()
        else:
            self.variables[var].value = value

    def getValue(self, var)
        if var not in self.variables.keys():
            print('Error in get(): variable {} has not been declared'.format(var))
        elseif (variables[var].value = None):
            print('Error in get(): variable {} has not been assigned a value'.format(var))
        else:
            return variables[var].value

    def getType(self, var)
        if var not in self.variables.keys():
            print('Error in get(): variable {} has not been declared'.format(var))
        else:
            return variables[var].type

