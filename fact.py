from termcolor import colored

class Fact:
    """
        This Class describes a Fact. It can be proved True
        or used to prove the validity of another fact.
    """

    def __init__(self, fact, engine):
        self.name = fact
        self.engine = engine
        self.checked = False

    def __str__(self):
        return f"Fact({self.name})"

    def resolve_to_true(self):
        "Backward resolution, return True or False"
        print(colored(f"Checking {self}", "yellow"))
        if self.engine.solve_fact(self):
            self.engine.add_facts('='+self.name)
            print(colored(f"{self} is then True\n", "yellow"))
            return True
        print(colored(f"{self} is then False\n", "yellow"))
        return False
