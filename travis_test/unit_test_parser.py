# Travis needs this to find parent python files
import sys
sys.path.extend(["../"])
import parser

data = [
    {
        "statement": "A <=> B",
        "result": True,
        "reversed": "B <=> A",
        "cut": {"rule": "A", "conclusion": "B"}
    },
    {
        "statement": "A + C <=> B",
        "result": True,
        "reversed": "B <=> A + C",
        "cut": {"rule": "A + C", "conclusion": "B"}
    },
    {
        "statement": "A | (A + A) <=> B",
        "result": True,
        "reversed": "B <=> A | (A + A)",
        "cut": {"rule": "A | (A + A)", "conclusion": "B"}
    },
    {
        "statement": "A <=> ! B",
        "result": True,
        "reversed": "! B <=> A",
        "cut": {"rule": "A", "conclusion": "! B"}
    },
]


def test_is_biconditial():
    for test in data:
        assert parser.is_biconditional(test['statement']) == test['result']

def test_reverse_statement():
    for test in data:
        assert parser.reverse_statement(test['statement']) == test['reversed']

def test_cut_statement():
    response = [x["cut"] for x in data]
    statements = [x["statement"].replace("<=>", "=>") for x in data]
    assert parser.cut_statement(statements) == response
