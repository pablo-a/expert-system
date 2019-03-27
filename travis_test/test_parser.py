import pytest
import os
import sys
# Travis needs this to find parent python files
sys.path.extend(["../"])
from exception import ParsingError
from parse import parse_file


def test_incorrect_files():
    list_files = [
        "",
        ".",
        "..",
        "/dev/random",
        "/dev/null",
        ".gitignore",
        "test_files"
    ]
    print("hello")
    run_tests(list_files)

def test_wrong_files():
    run_tests(get_files("./test_files", pattern="f_"))
    run_tests(get_files("./pablo_test/incorrect"))

def run_tests(file_list):
    for file_path in file_list:
        tab = []
        with pytest.raises(ParsingError):
            print(f"Testing file : {file_path}")
            parse_file(file_path, tab)


def get_files(path, pattern=""):
	files = []
	for file in os.listdir(path):
		file_path = path + "/" + file
		if os.path.isdir(file_path):
			files.extend(get_files(file_path))
		elif os.path.isfile(file_path) and pattern in file:
			files.append(file_path)
	return (files)
