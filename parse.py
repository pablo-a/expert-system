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
    #not_assigned(tab)
    validParenthesis(tab)
    # Check if all steps are here (rules, facts, target)
    min_step(tab)
    # Merge multiline facts/questions in 1 token
    concat_list(tab)

def del_same(tab):  # Delete same line in tab
	for val, second in enumerate(tab):
		for first in tab[val + 1:]:
			if first == second:
				tab.remove(first)

def validParenthesis(tab):
	for line in tab:
		if '(' in line or ')' in line:
			countop = line.count('(')
			countclose = line.count(')')
			if countop - countclose != 0:
				raise_parsing_error("Error: Missing parenthesis")
			if matchingParenthesis(line) == False:
				raise_parsing_error("Error: Bad parenthesis")
			
def matchingParenthesis(string):
	nb = 0
	balanced = True
	index = 0
	while index < len(string):
		token = string[index]
		if token == "(":
			nb += 1
		elif token == ")":
			nb -= 1
			if nb == -1:
				balanced = False
				break

		index += 1
	
	return balanced

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

def break_input_statement_type(input):
    """
        Return sorted statement from input file.
        Output : [[rules], [facts], [query]]
    """
    rules = []
    facts = []
    query = []

    for line in input:
        if ("=>" in line or "<=>" in line) and is_rule(line):
            rules.append(line)
        elif "=" in line:
            facts.append(line)
        elif "?" in line:
            query.append(line)

    return [rules, facts, query]

def is_rule(input):
	op = "=>"
	if "<=>" in input:
		op = "<=>"
	splitted = input.split(op)
	without_empty = list(filter(None, splitted))
	if len(without_empty) != 2:
		raise_parsing_error("Operator should have data on both side.") 