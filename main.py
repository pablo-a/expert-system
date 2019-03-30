import sys
# FIXME: rename parse module to something like lexer, syntax_checker, ...
import parse
import parser
from engine import Engine
from rules_json import rules_json
from exception import ParsingError

# 	List of all symbols possibility
operand_n = ["!", "^", "=>", "<=>", "(", ")", "+", "|"]


def main(file_path):
    tab = []

    # Parsing
    try:
        parse.parse_file(file_path, tab)
    except ParsingError as e:
        exit(e)

    # break into different type of statements
    rules, facts, query = parse.break_input_statement_type(tab)

    # setup engine
    engine = Engine()
    parser.setup_engine_rules(engine, rules)
    parser.setup_engine_facts(engine, facts)
    parser.setup_engine_query(engine, query)

    # Solving
    # rules_json(tab)
    # engine.solve()


def raise_parsing_error(msg):
    raise ParsingError(msg)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Error: Bad arguments")
    main(sys.argv[1])
