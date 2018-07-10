
# Authors: Charlie McDermitt
#          Eric Schneider
#          Corey Harris
# Class:   CS4308 - W01
#          Concepts of Programming Languages
# Title:   Final Project - Second Deliverable
# Date:    09 July 2018

# Scanner.py
# The Scanner class contains member variables and functions invoked by the Parser in order to connect with and interpret
# input file data and state machine logic. The overall functionality of the Scanner is made up of two primary operations,
# which are the initial parsing of the input file and filling of the scanner object's symbol table, and returning the most
# current lexeme and attributes to the Parser when called upon. The primary variables and functions are defined below:

# Member Variables:
#   tokens -> output array for tokens and data
#   symbol_table -> 2D array for lexeme attribute data. Position corresponds to line number and position
#   attributes -> list of lexeme attributes retrieved from state_machine logic, which make up symbol_table indexes
#   current_row/current_attribute -> incrementing symbol_table index for next lexeme to be passed to Parser
#   last_token -> most previously referenced token, saved for error checking
#   lex -> currently held lexeme of scanner to be passed to Parser
#   input_file/output_file -> variables for storing file paths

# Member Functions:
#   next(self): Set lex to next lexeme in symbol_table
#   peek(self): Return next lexeme to symbol_table, without setting lex. Used to conditional statement checking
#   last(self): Set last_token to position (current_attribute - 1)
#   fillSymbolTable(self): Perform initial parse of input file and fill symbol table. Called once if table is empty.
#   writeChangeLog(self): Create the output file of parsed data.


# imports
import sys
from state_machine import processLine
import csv

class Scanner:

    def __init__(self, infile):
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


    def start(self):
        self.fillSymbolTable()
        self.lex = self.symbol_table[0][0]
    # Name: next
    # Summary: Advance lex by one position in the row and save the new attribute list to self.lex
    #          If the current_attribute is greater than or equal to the length of the current row,
    #          the function increments the current_row and resets the current_attribute counter.
    #          If the current_row is greater than or equal to the length of the table, the function
    #          returns a null value, because the parser has reached the end of the file.
    # Returns: None.
    #          Function sets self.lex to new value
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

    # Name: peek
    # Summary: Returns the lexeme at position symbol_table[current_row][current_attribute + 1] if there is room in row
    #          Otherwise, it increments the row and returns the first index.
    # Returns: Next lexeme in table without setting lex
    def peek(self):
        if (len(self.symbol_table) == 0):
            self.fillSymbolTable()
        if (self.current_row >= len(self.symbol_table)):
            return (None, None, None, None)
        if self.current_attribute + 1 >= len(self.symbol_table[self.current_row]):
            if (self.current_row + 1 >= len(self.symbol_table)):
                return (None, None, None, None)
            return self.symbol_table[self.current_row + 1][0]
        else:
            if (self.current_row >= len(self.symbol_table)):
                return (None, None, None, None)
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

    # Name: fillSymbolTable
    # Summary: Invoked by __init__ if empty
    #          Parses through the input file saved to the Scanner object line by line
    #          Each line is sent to the State Machine processLine function, which fills the attributes list
    #          Once control has returned, the Scanner appends the new attributes list to symbol_table
    # Returns: None
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

    # Name: writeChangeLog
    # Summary: Open the output file path and write each index of the symbol_table and its data to the output file.
    # Returns: None
    def writeChangeLog(self):
        with open(self.output_file, 'w') as outfile:  # open output file
            writer = csv.writer(outfile)
            writer.writerow(["Value", "Type", "Line Number", "Line Position"])
            for i in range(0, len(self.symbol_table)):
                for j in range(0, len(self.symbol_table[i])):
                    self.symbol_table[i][j].extend([i, j])  # adds line number and position to each entry
                writer.writerows(self.symbol_table[i])  # writes each item in tokens to a row of the .csv
