class Engine():

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


class Fact():

    def __init__(self, fact):
        self.data = fact

    def resolve_to_true(self):
        return True
