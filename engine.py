class Engine:
    def __init__(self):
        self.rules = {}
        self.facts = []
        self.query = []

    def add_rule(self, tokenized_line):
        """
        Input: 1 file tokenized line :  A | B + C => D
        Output: data structure :       OR(A, AND(B, C))
        """
        pass

    def add_facts(self, tokenized_line):
        """
        Add facts to self.facts array
        Input: "=ABC"
        """
        pass

    def add_query(self, tokenized_line):
        """
        Add query item to self.query array
        Input: ?XZY
        """
        pass
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


class Fact:

    def __init__(self, fact, engine):
        self.name = fact
        self.engine = engine
        self.checked = False

    def __str__(self):
        return self.name

    def resolve_to_true(self):
        return self.engine.solve_fact(self)
        
