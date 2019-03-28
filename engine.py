import logging

class Engine:
    def __init__(self):
        self.rules = {}
        self.facts = set()
        self.query = []
        self.already_checked = []

    def add_rule(self, tokenized_line):
        """
        Input: 1 file tokenized line :  A | B + C => D
        Output: data structure :       OR(A, AND(B, C))
        """
        pass

    def add_facts(self, tokenized_line, empty=False):
        """
        Add facts to self.facts array
        Input: "=ABC"
        """
        if empty:
            self.facts = set()

        if not tokenized_line.startswith("="):
            return
        for char in tokenized_line[1:]:
            new_fact = Fact(char, self)
            self.facts.add(new_fact)

    def add_query(self, tokenized_line, empty=False):
        """
        Add query item to self.query array
        Input: ?XZY
        """
        if empty:
            self.query = []
            
        if not tokenized_line.startswith("?"):
            return
        for char in tokenized_line[1:]:
            new_fact = Fact(char, self)
            self.query.append(new_fact)

########################## THE METHOD ####################################
    def solve(self):
        solution = []
        for query in self.query:
            solution.append(self.solve_fact(query))
            self.already_checked = []
        return solution

    def solve_fact(self, fact):
        if fact.name in self.already_checked:
            print("\tAlready been here, stopping.")
            return False
        self.already_checked.append(fact.name)

        if self.fact_is_true(fact):
            return True

        # Fetch a condition of truth
        try:
            rule = self.get_rule(fact)
        except KeyError: # means no precendence rule.
            print(f"\tno rule for fact {fact}")
            return False

        print(f"\trule found for fact {fact} : {rule}")
        # If dependency is just a Fact (A => B), recursive call
        if isinstance(rule, Fact):
            return self.solve_fact(rule)
        # else it is operators to resolve.
        return rule.resolve_to_true()

###########################################################################

    def fact_is_true(self, fact):
        # Check if Fact already in knowledge base
        for elem in self.facts:
            if fact.name == elem.name:
                print(f"\tfact {fact.name} is in knowledge base")
                return True
        print(f"\tfact {fact.name} is not in knowledge base")
        return False

########################################################################

    def get_rule(self, fact):
        return self.rules[fact.name]

    def __str__(self):
        string = "Knowledge base :\n"
        for elem in self.facts:
            string += f"\t{elem}\n"

        string += "\n"
        string += "Rules :\n"
        for elem in self.rules:
            string += f"\t{elem} : {self.rules[elem]}\n"

        string += "\n"
        string += "Query :\n"
        for elem in self.query:
            string += f"{elem}"
        return string


class Fact:

    def __init__(self, fact, engine):
        self.name = fact
        self.engine = engine
        self.checked = False

    def __str__(self):
        return self.name

    def resolve_to_true(self):
        return self.engine.solve_fact(self)
        
