import sys
# Travis needs this to find parent python files
sys.path.extend(["../"])

from engine import Engine, Fact
from operations import And, Or

# TESTING
my_engine = Engine()

# ADD FACTS
# => False
my_engine.add_facts("=ABCD")
my_engine.add_facts("=Y")
# my_engine.add_facts("=E")
# => False
# engine.add_facts("=AZDE")

# ADD MAIN RULE
rule_A = And(
    And(
        Fact("A", my_engine),
        Or(
            Fact("B", my_engine),
            Fact("Z", my_engine)
        )
    ),
    And(
        Fact("C", my_engine),
        And(
            Fact("D", my_engine),
            Fact("E", my_engine)
        )
    )
)

query = Fact("X", my_engine)
my_engine.rules[query.name] = rule_A

#Backtracking
second_rule = Fact("Y", my_engine)
query2 = Fact("E", my_engine)
my_engine.rules[query2.name] = second_rule

#Backtracking
second_rule = Fact("E", my_engine)
query2 = Fact("Y", my_engine)
my_engine.rules[query2.name] = second_rule

rule_A.flatten()


def test_simple():
    print(my_engine)
    # Already in Facts
    my_engine.add_query("?A")
    assert my_engine.solve() == [True]
    
def test_backward():
    # 2 steps backward
    my_engine.add_query("?X", empty=True)
    assert my_engine.solve() == [True]

def test_infinite_loop():
    # Infinite loop
    pass