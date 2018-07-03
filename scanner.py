#imports
import sys
from state_machine import processLine

class Scanner:
    # List of output tokens and line numbers
    tokens = []
    # 2D symbol table array to hold attribute data
    # Rows correspond to line number, and columns to line position
    # Initialized as one-dimensional list. Rows added for each attribute list
    symbol_table = []
    # Attributes list to hold ID, Value, and Type of each keyword in a line
    attributes = []
    # Integer counter for current row current attribute
    current_row = 0
    current_attribute = 0
    last_token = ()
    def getNextToken(self):
        global last_token
        target_token = []
        if (len(self.symbol_table) == 0):
            self.fillSymbolTable()
        if (self.current_row >= len(self.symbol_table)):
             return (None, None, None, None)
        target_token = self.symbol_table[self.current_row][self.current_attribute]
        self.last_token = target_token
        self.current_attribute = self.current_attribute + 1
        if self.current_attribute >= len(self.symbol_table[self.current_row]):
            self.current_row = self.current_row + 1
            self.current_attribute = 0
        return target_token

    def getCurrentToken(self):
        return self.last_token
	
    def fillSymbolTable(self):
        linenum = 0
        with open(sys.argv[1]) as infile:  # open the file, sys.argv[1] is the first command line argument
            print(sys.argv[1])
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

    def writeChangeLog(self):
        with open('output_scanned.csv', 'w') as outfile:  # open output file
            # writer = csv.writer(outfile)
            writer.writerow(["ID", "Value", "Type", "Line Number", "Line Position"])
            for i in range(0, len(self.symbol_table)):
                for j in range(0, len(self.symbol_table[i])):
                    self.symbol_table[i][j].extend([i, j])  # adds line number and position to each entry
                writer.writerows(self.symbol_table[i])  # writes each item in tokens to a row of the .csv
