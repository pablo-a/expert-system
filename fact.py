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
        if self.engine.solve_fact(self):
            self.engine.add_facts('='+self.name)
            return True
        return False
