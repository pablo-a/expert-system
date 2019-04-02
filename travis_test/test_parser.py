import pytest
import os
import sys
import logging

# Travis needs this to find parent python files
sys.path.extend(["../", "./travis_test/", "../../"])
# from parser import setup_engine_facts, setup_engine_query, setup_engine_rules
from exception import ParsingError
from parse import parse_file, break_input_statement_type
from parser import setup_engine_facts, setup_engine_query, setup_engine_rules
import engine


def test_incorrect_files():
    list_files = ["", ".", "..", "/dev/random", "/dev/null", ".gitignore", "test_files"]
    run_tests(list_files)


def test_wrong_files():
    run_tests(get_files("./travis_test/test_files", pattern="f_"))
    run_tests(get_files("./travis_test/pablo_test/incorrect", pattern="test_"))


def run_tests(file_list):
    for file_path in file_list:
        tab = []
        with pytest.raises(ParsingError):
            logging.critical("TEST TEST")
            print(f"Testing file : {file_path}")
            parse_file(file_path, tab)
            rules, facts, query = break_input_statement_type(tab)

            # setup engine
            my_engine = engine.Engine()
            # re parse rules
            setup_engine_rules(my_engine, rules)
            setup_engine_facts(my_engine, facts)
            setup_engine_query(my_engine, query)


def get_files(path, pattern=""):
    files = []
    for file in os.listdir(path):
        file_path = path + "/" + file
        if os.path.isdir(file_path):
            files.extend(get_files(file_path))
        elif os.path.isfile(file_path) and pattern in file:
            files.append(file_path)
    return files
