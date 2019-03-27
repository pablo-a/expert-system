import sys
import parse
from rules_json import rules_json
from exception import ParsingError

#	List of all symbols possibility
operand_n = ['!', '^', "=>", "<=>", '(', ')', '+', '|']

def main(file_path):
	tab = []

	# Parsing
	try:
		parse.parse_file(file_path, tab)
	except ParsingError as e:
		exit(e)

	# Solving
	rules_json(tab)
		

def raise_parsing_error(msg):
	raise ParsingError(msg)


if __name__ == '__main__':
	if len(sys.argv) != 2:
		sys.exit("Error: Bad arguments")
	main(sys.argv[1])
