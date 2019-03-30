import logging
from fact import Fact


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

    ########################## SOLVING ####################################
    def solve(self):
        # FIXME: make solution an instance attribute ?
        solution = []
        for query in self.query:
            solution.append(self.solve_fact(query))
            self.already_checked = []
        return solution

    def solve_fact(self, fact):
        """
            Check if a Fact is true or not based on rules & 
            knowledge base. Returns True or False
        """
        # Stop if we have already been here
        if fact.name in self.already_checked:
            print("\tAlready been here, stopping.")
            return False
        self.already_checked.append(fact.name)

        # Check if Fact in knowledge Base
        if self.fact_is_true(fact):
            return True

        # find a rule to prove fact.
        try:
            rule = self.get_rule(fact)
        except KeyError:  # means no precendence rule.
            print(f"\tno rule for fact {fact}")
            return False

        print(f"\trule found for fact {fact} : {rule}")
        # If dependency is just a Fact (A => B), recursive call
        if isinstance(rule, Fact):
            return self.solve_fact(rule)
        # else it is operators to resolve.
        return rule.resolve_to_true()

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

    ###################### Engine Printing ######################

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
