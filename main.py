import sys
import os.path
import parse
from rules_json import rules_json

#	List of all symbols possibility
operand_n = ['!', '^', "=>", "<=>", '(', ')', '+', '|']

def main():
	tab = []

	if len(sys.argv) == 2:
		check(tab)
		if not tab:
			error_case("Error: Empty file")
		for id,e in enumerate(tab):
			tab[id] = translate(e)
		parse.parse_tab(tab)
		rules_json(tab)
	else:
		error_case("Error: Bad arguments")

def error_case(msg):
        print(msg)
        sys.exit()

def check(tab):     #   Check if open file is possible and if eatch line is valide
	input_file = 0
	if os.path.isfile(sys.argv[1]):
		try:
			input_file = open(sys.argv[1], "r")
		except IOError as e:
			error_case(f"Error: File can't by open : {e}")
		for line in input_file:
			remove_empty_and_comments(tab, line)
	else:
		error_case("Error: File doesn't exist")

def remove_empty_and_comments(tab, line):
	# don't care for empty lines
	if is_empty(line):
		return

	# remove leading/trailing whitespaces
	line = line.strip()

	# remove comment parts.
	if is_comment(line):
		line_without_comment = line.split("#")[0]
		if (line_without_comment.strip() == ""):
			return
		tab.append(line_without_comment)
	else:
		tab.append(line)

def is_comment(line):
	return True if "#" in line else False

def is_empty(line):
	return True if line == "\n" else False

def translate(tab):         #   Tranform all litteral expression in symbol expression
	
	#	List of literal Symbols
	operand_l = ["not", "xor", "implies", "if and only if", '(', ')', "and", "or"]

	for i in operand_l:
		if i in tab.lower():
			tab = tab.replace(i, operand_n[operand_l.index(i)])
	return tab.strip()


if __name__ == '__main__':
    main()
