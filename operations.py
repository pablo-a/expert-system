class Operator:
    "Defines an operator : AND, OR, NOT, XOR, ..."

    def __init__(self, left_operand, right_operand):
        self.operands = []
        self.left_operand = left_operand
        self.right_operand = right_operand


class And(Operator):
    def simplify(self):
        """
            Simplify nested structure of same types
            AND(A, AND(B, AND(C, D))) => AND(A, B, C)
        """
        pass

    def resolve_to_true(self):
        """
            Check if the different operands resolve to True
            A = B = C = True => AND(A, B, C) = True 
        """
        for elem in self.operands:
            if not elem.resolve_to_true():
                return False
        return True
