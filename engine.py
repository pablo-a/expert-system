import logging
import operations
from termcolor import colored
from fact import Fact
from exception import ParsingError


class Engine:
    def __init__(self):
        self.rules = {}
        self.facts = set()
        self.query = []
        self.already_checked = []

####################### SETTING UP ENGINE RULES, FACTS, QUERY #################

    def add_rule(self, rule, condition):
        """
            Input: Fact(A) , Or("B", "C")
            Output: data structure :       OR(A, AND(B, C))
        """
        if rule.name in self.rules:
            self.add_additional_rule(rule, condition)
        else:
            self.rules[rule.name] = condition

    def add_additional_rule(self, rule, condition):
        "In case of different rules for same fact."
        old_rule = self.rules[rule.name]
        new_rule = operations.Or(old_rule, condition)
        # flatten nested Or's.
        new_rule.flatten()
        self.rules[rule.name] = new_rule

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
            if char in self.facts:
                raise ParsingError(f"Facts must be unique : {char} is present twice!")
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
            if char in self.facts:
                raise ParsingError(f"Query must be unique : {char} is present twice!")
            new_fact = Fact(char, self)
            self.query.append(new_fact)

    ########################## SOLVING ########################################
    def solve(self):
        for query in self.query:
            print(colored(f"\nAnswer for {query} :", "green"))
            solution = self.solve_fact(query)
            if solution:
                self.add_facts(query.name)
            print(colored(f"{query} is then {solution}", "red"))
            self.already_checked = []
            
    def solve_fact(self, fact):
        """
            Check if a Fact is true or not based on rules & 
            knowledge base. Returns True or False
        """

        # Check if Fact in knowledge Base
        if self.fact_is_true(fact):
            return True

        # Stop if we have already been here
        if fact.name in self.already_checked:
            print("\tAlready been here, stopping.")
            return False
        self.already_checked.append(fact.name)
        
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
        string = "Knowledge base :"
        for elem in self.facts:
            string += f" {elem}"

        string += "\n"
        string += "Rules :\n"
        for elem in self.rules:
            string += f"\t{elem} : {self.rules[elem]}\n"

        string += "\n"
        string += "Query :"
        for elem in self.query:
            string += f" {elem}"
        return string
