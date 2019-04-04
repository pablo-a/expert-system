from logging.handlers import RotatingFileHandler
from termcolor import colored
import sys
import logging
# FIXME: rename parse module to something like lexer, syntax_checker, ...
import parse
import parser
from engine import Engine
from exception import ParsingError

# 	List of all symbols possibility
operand_n = ["!", "^", "=>", "<=>", "(", ")", "+", "|"]


def main(file_path):
    tab = []

    setup_logging()

    try:
        # Parsing
        parse.parse_file(file_path, tab)
        # break into different type of statements
        rules, facts, query = parse.break_input_statement_type(tab)
        logging.info(colored(f"\nrules : {rules}\nfacts: {facts}\nquery: {query}\n", "yellow"))

        # setup engine
        engine = Engine()
        # re parse rules
        parser.setup_engine_rules(engine, rules)
        parser.setup_engine_facts(engine, facts)
        parser.setup_engine_query(engine, query)
    except ParsingError as e:
        exit(e)

    logging.info(colored(f"\n{engine}", "cyan"))

    # Solving
    return engine.solve()

def setup_logging():
    # création de l'objet logger qui va nous servir à écrire dans les logs
    logger = logging.getLogger()
    # on met le niveau du logger à DEBUG, comme ça il écrit tout
    logger.setLevel(logging.CRITICAL)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.exit("Error: Bad arguments")
    main(sys.argv[1])
