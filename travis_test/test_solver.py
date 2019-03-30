import sys
# Travis needs this to find parent python files
sys.path.extend(["../"])

from engine import Engine, Fact
from operations import And, Or
from termcolor import colored


def log_engine(run_test):
    def wrap():
        print(colored(f"\n\nTEST : {run_test.__name__}\n", "red"))
        print(colored("\nSolution steps :\n\t", 'green'))
        run_test()
        print(colored("\nFacts :\n", 'green'))
        print(colored(f"\n{my_engine}", 'magenta'))
        print(colored(f"\nTest passed ? ", "yellow"), end="")
    return wrap

# TESTING
my_engine = Engine()

# ADD FACTS
my_engine.add_facts("=ABCD")
my_engine.add_facts("=Y")

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

@log_engine
def test_simple():
    # Already in Facts
    my_engine.add_query("?A")
    assert my_engine.solve() == [True]
    
@log_engine
def test_backward():
    # 2 steps backward
    my_engine.add_query("?X", empty=True)
    assert my_engine.solve() == [True]

@log_engine
def test_infinite_loop():
    "Infinite Loop if try to resolve"
    # reset facts.
    my_engine.add_facts("=", empty=True)
    my_engine.add_query("?Y", empty=True)
    assert my_engine.solve() == [False]

@log_engine
def test_same_conclusion():
    "several rules for 1 conclusion"
    my_engine.add_facts("=Q")
    my_engine.add_query("?X", empty=True)
    #add new rule : Q => X
    f = Fact("X", my_engine)
    rule = Fact("Q", my_engine)
    my_engine.add_rule(f, rule)
    #solve
    assert my_engine.solve() == [True]

@log_engine
def test_same_conclusion_2():
    "several nested rules for 1 conclusion"
    my_engine.add_facts("=R", empty=True)
    # Add new rule : : R | S => X
    target = Fact("X", my_engine)
    new_condition = Or(Fact("R", my_engine), Fact("S", my_engine))
    my_engine.add_rule(target, new_condition)

    #solve
    assert my_engine.solve() == [True]

