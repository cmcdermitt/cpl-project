# imports
import sys
from state_machine import processLine
import csv


class Scanner:

    def __init__(self, infile, outfile='output_scanned.csv'):
        # List of output tokens and line numbers
        self.tokens = []
        # 2D symbol table array to hold attribute data
        # Rows correspond to line number, and columns to line position
        # Initialized as one-dimensional list. Rows added for each attribute list
        self.symbol_table = []
        # Attributes list to hold value and type of each keyword in a line
        self.attributes = []
        # Integer counter for current row current attribute
        self.current_row = 0
        self.current_attribute = 0
        self.last_token = ()
        self.lex = ()
        self.input_file = infile
        self.output_file = outfile

    def next(self):  # advances lex
        if (len(self.symbol_table) == 0):
            self.fillSymbolTable()
        if (self.current_row >= len(self.symbol_table)):
            return (None, None, None, None)
        self.last_token = self.lex
        self.current_attribute = self.current_attribute + 1
        if self.current_attribute >= len(self.symbol_table[self.current_row]):
            self.current_row = self.current_row + 1
            self.current_attribute = 0
        if(self.current_row >= len(self.symbol_table)):
            return(None,None,None,None)
        self.lex = self.symbol_table[self.current_row][self.current_attribute]

    def peek(self):  # returns next token, but doesn't advance lex - doesn't currently work
        if (len(self.symbol_table) == 0):
            self.fillSymbolTable()
        if (self.current_row >= len(self.symbol_table)):
            return (None, None, None, None)
        if self.current_attribute + 1 >= len(self.symbol_table[self.current_row]):
            return self.symbol_table[self.current_row + 1][0]
        else:
            return self.symbol_table[self.current_row][self.current_attribute + 1]

    # A recursive definition always has to peek one ahead to
    # decide if it is going to continue repeating its right hand
    # definition. When a recursive definition finishes, it is
    # one token past where it should be. Thus, all recursive definitions
    # should rewind one token after completion <-- THIS IS OLD
    def last(self):
        if (self.current_attribute > 0):
            self.current_attribute -= 1
        elif (self.current_attribute == 0 and self.current_row > 0):
            self.current_row -= 1
            self.current_attribute = len(self.symbol_table[self.current_row]) - 1
        else:
            print('Invalid rewind')

        self.last_token = self.symbol_table[self.current_row][self.current_attribute]

    def fillSymbolTable(self):
        linenum = 0
        with open(self.input_file) as infile:  # open the file, sys.argv[1] is the first command line argument
            print(self.input_file)
            for line in infile:
                linenum += 1
                # ProcessLine returns list of lists containing keyword attributes
                #  Structure of single index: [ID, Value, Type]
                #  Note: "Type" is represented by the int equivalent of its
                #  position in the keywords dictionary
                attributes = processLine(line)
                self.symbol_table.append(attributes)
                for list in self.symbol_table:
                    if len(list) == 0:
                        self.symbol_table.remove(list)
                        for i in range(0, len(attributes)):
                            print(attributes[i])

    def start(self):
        self.fillSymbolTable()
        self.lex = self.symbol_table[0][0]

    def writeChangeLog(self):
        with open(self.output_file, 'w') as outfile:  # open output file
            writer = csv.writer(outfile)
            writer.writerow(["Value", "Type", "Line Number", "Line Position"])
            for i in range(0, len(self.symbol_table)):
                for j in range(0, len(self.symbol_table[i])):
                    self.symbol_table[i][j].extend([i, j])  # adds line number and position to each entry
                writer.writerows(self.symbol_table[i])  # writes each item in tokens to a row of the .csv
