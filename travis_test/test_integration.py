import pytest
import sys

sys.path.extend(["../", "./travis_test/", "../../"])
from main import main as expert_system

list_file = {
    "and": "./travis_test/correction_tests/and",
    "or": "./travis_test/correction_tests/or",
    "xor": "./travis_test/correction_tests/xor",
    "not": "./travis_test/correction_tests/not",
    "parentheses": "./travis_test/correction_tests/parentheses",
    "same": "./travis_test/correction_tests/same"
}

def test_and():
    test_file = list_file['and']
    solution = get_solution(test_file)
    assert expert_system(test_file) == solution


def test_or():
    test_file = list_file['or']
    solution = get_solution(test_file)
    assert expert_system(test_file) == solution


def test_xor():
    test_file = list_file['xor']
    solution = get_solution(test_file)
    assert expert_system(test_file) == solution


def test_not():
    test_file = list_file['not']
    solution = get_solution(test_file)
    assert expert_system(test_file) == solution

def test_parenthesis():
    test_file = list_file['parentheses']
    solution = get_solution(test_file)
    assert expert_system(test_file) == solution


def test_same():
    test_file = list_file['same']
    solution = get_solution(test_file)
    assert expert_system(test_file) == solution


# Solution format should be on first line :
#solution=[True,False,...]
def get_solution(file_path):
    with open(file_path, 'r') as f:
        first_line  = f.readline()
        print(first_line)
        splitted = first_line.split("=")[1].split(",")
        print(splitted)
        mList = [True if e == "True" or e == "True\n" else False for e in splitted]
        return mList
