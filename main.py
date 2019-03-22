import sys
import os.path
from rules_json import rules_json

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

def del_same(tab):      #   Delete same line in tab
	for	val,second in enumerate(tab):
		for first in tab[val + 1:]:
			if first == second:
				tab.remove(first)

def checkTwoSide(string):       #   Split the string at the delimiter
    #   splitAffectation used to contain first and last part of string. toFind used like delimiter
    splitAffectation = toFind = ""
    #   Use like a falg variable
    whichCase = 0

    toFind = "=>" if string.find("<=>") == -1 else "<=>"
    splitAffectation = string.split(toFind)
    for i in splitAffectation:
        whichCase = missingBracket(i)
        if whichCase == 1:
	    error_case("Error: Missing bracket in [" + string + ']')
        elif whichCase == 2:
	    error_case("Error: Missing a ')' bracket in [" + string + ']')
        elif whichCase == 3:
	    error_case("Error: Missing a '(' bracket in [" + string + ']')
    return 0

def not_assigned(tab):      #	Check if there are a good assignation expression
    test = 0
    for lineOfArray in tab:
        if not checkTwoSide(lineOfArray):
            for eatchChar in operand_n:
                if eatchChar in lineOfArray and eatchChar not in ['(', ')']:
                    lineOfArray.strip()
                    #print lineOfArray

def missingBracket(string):     #   Check if missing bracket in string
    #	Use to find multiple pair bracket
    counterBracket = 0 

    for i in string:
        if i == '(':
            counterBracket += 1
        elif i == ')':
            counterBracket -= 1
    if counterBracket:
        return 2 if counterBracket > 0 else 3
    return bracketBadFormat(string)

def bracketBadFormat(string):       #   Check if open bracket is before close bracket
    #	Flag to know if steps are pass
    flag = 0

    for i in string:
        if i in ['(', ')']:
            if i == ')' and not (flag & 1):
                error_case("Error: Declaration of '" + i +
                "' bracket before '(' in [" + i + "]")
            flag |= (1 << 0 if i == '(' else 1 << 1)
    return 0 if (flag & 1) and (flag & 2) or not flag else 1

def	min_step(tab):      #	Check if there are a minimum steps to be resolv
	#	Flag to know if steps are pass
	flag = 0
	#	Array to errors list
	err = ["Error: Missing ", " expression", "X => Y", "=XXX", "?XXX"]

	for i in tab:
		for j in operand_n:
			if not flag and j in i:
				flag |= 1 << 0
		if i[0] in ['?', '='] and i[1].isalpha():
			flag |= (1 << 2 if i[0] in '?' else 1 << 1)
	if not ((flag & 1) and (flag & 2) and (flag & 4)):
		if not (flag & 1):
			print err[0] + err[2] + err[1]
		if not (flag & 2):
			print err[0] + err[3] + err[1]
		if not (flag & 4):
			print err[0] + err[4] + err[1]
		sys.exit()

def	split_tab(tab, cut_list):       #   Split all tab by space char
	for i in tab:
		cut_list.extend(i.split(' '))

def special_case(string):       #   Check if the element is a "=VAR" or "?VAR"
        #expression = inhibit_bracket(string)
	expression = string
	if expression[0] in ['?', '='] and expression[1:].isalpha():
		return 1
	elif expression[0] == '!' and expression[1].isalpha() and len(expression) == (2 if string == expression else 1):
                #print expression
		return 1
#	elif (expression[len(expression) - 1] == ')'
#		and expression[:len(expression) - 1].isalpha):
#                print expression
#		return 1
	return 0

def	check_lexic(cut_list):      #   Check if the string is lexical correct
	for j in cut_list:
            if ((j not in operand_n) and not j.isalpha() and
		not special_case(j)) or (len(j) > 1 and j.isalpha()):
		error_case("Error: Bad character [" + j + ']')

#def inhibit_bracket(string):        #  Return a string whiout bracket to test the element
#        newString = ""

#        for i in string:
#            if i not in ['(', ')']:
#                newString += i
#        return newString

def	concat_list(cut_list):      #   Check and concatenate the initialisations and question lines in tab
	for index, this in enumerate(cut_list):
	    for that in cut_list[index + 1:]:
			if (this[0] in ['=', '?']) and (this[0] == that[0]) and this[1:].isalpha():
				if (this == that):
					cut_list.remove(that)
					break
				cut_list[index] += that[1:]
				cut_list.remove(that)

def parse_tab(tab):
	cut_list = []

	del_same(tab)
	not_assigned(tab)
	min_step(tab)
	split_tab(tab, cut_list)
	#print("before: ", cut_list)
	#check_lexic(cut_list)
	concat_list(cut_list)
	#print("afteeeeeeer")
	#print("after: ", cut_list)
	tab = cut_list

def main():
	tab = []

	if len(sys.argv) == 2:
		check(tab)
		if not tab:
			error_case("Error: Empty file")
		for id,e in enumerate(tab):
			tab[id] = translate(e)
		parse_tab(tab)
		rules_json(tab)
	else:
		error_case("Error: Bad arguments")

if __name__ == '__main__':
    main()
