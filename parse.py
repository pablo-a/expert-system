from main import operand_n, raise_parsing_error
from exception import ParsingError
import sys
import os

def parse_file(file_path, tab):
    check(file_path, tab)
    if not tab:
        raise_parsing_error("Error: Empty file")
    for id, e in enumerate(tab):
        tab[id] = translate(e)
    parse_tab(tab)

# Check if open file is possible and if eatch line is valide
def check(file_path, tab):
	input_file = 0
	if os.path.isfile(file_path):
		try:
			input_file = open(file_path, "r")
		except IOError as e:
			raise_parsing_error(f"Error: File can't by open : {e}")
		for line in input_file:
			remove_empty_and_comments(tab, line)
	else:
		raise_parsing_error("Error: File doesn't exist")

def parse_tab(tab):
    # rules must be unique
    del_same(tab)
    # parenthesis analysis
    not_assigned(tab)
    # Check if all steps are here (rules, facts, target)
    min_step(tab)
    # Merge multiline facts/questions in 1 token
    concat_list(tab)

def del_same(tab):  # Delete same line in tab
	for val, second in enumerate(tab):
		for first in tab[val + 1:]:
			if first == second:
				tab.remove(first)

def not_assigned(tab):  # Check if there are a good assignation expression
    for lineOfArray in tab:
        # FIXME : checkTwoSide does not return anything but 0
        if not checkTwoSide(lineOfArray):
            for eatchChar in operand_n:
                if eatchChar in lineOfArray and eatchChar not in ['(', ')']:
                    lineOfArray.strip()
                    #print lineOfArray

def checkTwoSide(string):  # Split the string at the delimiter
    # splitAffectation used to contain first and last part of string.
    splitAffectation = ""
    # whichCase used like a falg variable
    whichCase = 0
    # toFind used like delimiter
    toFind = "=>" if string.find("<=>") == -1 else "<=>"

    splitAffectation = string.split(toFind)
    for i in splitAffectation:
        whichCase = missingBracket(i)
        # FIXME : case 1 never appears.
        if whichCase == 1:
	        raise_parsing_error("Error: Missing bracket in [" + string + ']')
        elif whichCase == 2:
	        raise_parsing_error("Error: Missing a ')' bracket in [" + string + ']')
        elif whichCase == 3:
	        raise_parsing_error("Error: Missing a '(' bracket in [" + string + ']')
    return 0

def missingBracket(string):  # Check if missing bracket in string
    #	Use to find multiple pair bracket
    counterBracket = 0

    for i in string:
        if i == '(':
            counterBracket += 1
        elif i == ')':
            counterBracket -= 1
    if counterBracket:
        # FIXME: What does this mean ?
        return 2 if counterBracket > 0 else 3
    return bracketBadFormat(string)

def bracketBadFormat(string):  # Check if open bracket is before close bracket
    #	Flag to know if steps are pass
    flag = 0
    empty = "()"

    if empty in string:
        raise_parsing_error(f"Error: Bad parenthesis in \"{string}\"")
    for i in string:
        if i in ['(', ')']:
            if i == ')' and not (flag & 1):
                raise_parsing_error(f"Error: Declaration of ')' bracket before '(' in \"{string}\"")
            elif i == ')':
                flag |= 2
            elif i == '(':
                flag |= 1
    return 0 if (flag & 1) and (flag & 2) or not flag else 1

def min_step(tab):  # Check if there are a minimum steps to be resolv
	#	Flag to know if steps are pass
	flag = 0
	#	Array to errors list
	err = ["Error: Missing ", " expression", "X => Y", "=XXX", "?XXX"]

	for line in tab:
		for operator in operand_n:
			if not flag and operator in line:
				flag |= 1
		if line == "=" or (line[0] in ['?', '='] and line[1].isalpha()):
			flag |= (4 if line[0] == '?' else 2)
	if not ((flag & 1) and (flag & 2) and (flag & 4)):
		if not (flag & 1):
			raise_parsing_error(err[0] + err[2] + err[1])
		if not (flag & 2):
			raise_parsing_error(err[0] + err[3] + err[1])
		if not (flag & 4):
			raise_parsing_error(err[0] + err[4] + err[1])
        
def concat_list(cut_list):  # Check and concatenate the initialisations and question lines in tab
    for index, token in enumerate(cut_list):
        if not (token[0] in ['=', '?']) or token == "=":
            continue
        for next_token in cut_list[index + 1:]:
            if (token[0] == next_token[0]) and token[1:].isalpha():
                if (token == next_token):
                    cut_list.remove(next_token)
                    break
                cut_list[index] += next_token[1:]
                cut_list.remove(next_token)


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


def translate(tab):  # Tranform all litteral expression in symbol expression

	#	List of literal Symbols
	operand_l = ["not", "xor", "implies", "if and only if", '(', ')', "and", "or"]

	for i in operand_l:
		if i in tab.lower():
			tab = tab.replace(i, operand_n[operand_l.index(i)])
	return tab.strip()
