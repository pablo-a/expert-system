import sys
import os.path

#	List of all symbols possibility
operand_n = ['!', '^', "=>", "<=>", '(', ')', '+', '|']

def error_case(msg):
        print msg
        sys.exit()

def check(tab):     #   Check if open file is possible and if eatch line is valide
	var = 0
	if os.path.isfile(sys.argv[1]):
		try:
			var = open(sys.argv[1], "r")
		except IOError as e:
			error_case("Error: File can't by open")
		for i in var:
			tmp = valide_line(i)
			if tmp > 0:
			 	tab.append(i[:tmp])
	else:
		error_case("Error: File doesn't exist")

def valide_line(line):      #   Check if there are comment in line
	tmp = line.find("#")
	if tmp == -1:
		return None
	else:
		return tmp

def translate(tab):         #   Tranform all litteral expression in symbol expression
	
	#	List of literal Symbols
	operand_l = ["not", "xor", "implies", "if and only if", '(', ')', "and", "or"]

	for i in operand_l:
		if i in tab.lower():
			flag = 1
			tab = tab.replace(i, operand_n[operand_l.index(i)])
	return tab.strip()

def main():
    tab = []

    if len(sys.argv) == 2:
        check(tab)
        #print(tab)
        if not tab:
            error_case("Error: Empty file")
        for id, e in enumerate(tab):
            tab[id] = translate(e)
        #parse(tab)
        print(tab)
    else:
        error_case("Error: Bad arguments")
        
if __name__ == '__main__':
    main()
