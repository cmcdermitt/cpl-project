# Authors: Charlie McDermitt
#          Eric Schneider
#          Corey Harris
# Class:   CS4308 - W01
#          Concepts of Programming Languages
# Title:   Final Project - Second Deliverable
# Date:    09 July 2018

import scl_parser
import sys

def main():
    lex_tree = scl_parser.parse()
    print(printAnnotatedTree(lex_tree, 0, True))


# Prints out the tree using tabs to represent children
def printTree(tree_list, tab, out_string = ''):
	if(len(tree_list) == 0):
		return
	if len(sys.argv) > 2: #if there's an output file name
		out_string = out_string + returnTabs(tab) + tree_list[0] + '\n' # Print out the first item in the list; this is the parent node
		if(len(tree_list) == 1):
			return
		for x in range(1, len(tree_list)): # Print out all of its children
			if(isinstance(tree_list[x], str)): # If the child is a string, print it out
				out_string = out_string + returnTabs(tab) + tree_list[x] + '\n'
			elif(isinstance(tree_list[x], list)): #If the child is a list, indent by 1 and print out that list
				out_string = printTree(tree_list[x], tab + 1, out_string)
			else:
				out_string = out_string + returnTabs(tab + 1) + str(tree_list[x]) + '\n'
		with open(sys.argv[2], 'w') as outfile:
			outfile.write(out_string)
	return out_string

#Prints a version of the tree with more information
def printAnnotatedTree(tree_list, tab, printTree = False, out_string = ''):
	if(len(tree_list) == 0):
		return out_string
	out_string +=  returnTabs(tab) + ( ('Enter <' + tree_list[0] + '>\n'))
	if(len(tree_list) == 1):
		return out_string
	for x in range(1, len(tree_list)):
		if(isinstance(tree_list[x], str)):
			out_string +=  returnTabs(tab) + tree_list[x] + '\n'
		elif(isinstance(tree_list[x], list)):
			out_string = printAnnotatedTree(tree_list[x],tab + 1, False, out_string)
		else:
			out_string +=  returnTabs(tab + 1) + 'Type is ' + str(tree_list[x][scl_parser.lex_en['type']]) + ' Value is ' + str(tree_list[x][scl_parser.lex_en['value']])
			out_string += ' at line ' + str(tree_list[x][scl_parser.lex_en['line_num']]) + '\n'

	return out_string

# Returns number of tabs
def returnTabs(tabNum):
	tabs = ''
	for i in range(tabNum):
		tabs = tabs + '    '
	return tabs

if __name__ == '__main__':
	main()