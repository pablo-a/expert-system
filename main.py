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

			# don't care for empty lines
			if empty_line(line):
				continue

			# remove leading/trailing whitespaces
			line = line.strip()

			# remove comment parts.
			tmp = valide_line(line)
			if tmp > 0:
				tab.append(line[:tmp])
	else:
		error_case("Error: File doesn't exist")

def valide_line(line):      #   Check if there are comment in line
	tmp = line.find("#")
	if tmp == -1:
		return len(line)
	else:
		return tmp

def translate(tab):         #   Tranform all litteral expression in symbol expression
	
	#	List of literal Symbols
	operand_l = ["not", "xor", "implies", "if and only if", '(', ')', "and", "or"]

	for i in operand_l:
		if i in tab.lower():
			tab = tab.replace(i, operand_n[operand_l.index(i)])
	return tab.strip()

def empty_line(line):
	return True if line == "\n" else False


if __name__ == '__main__':
    main()
