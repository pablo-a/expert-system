from engine import Engine, Fact
from functools import reduce

class Operator:
    "Defines an operator : AND, OR, NOT, XOR, ..."

    def __init__(self, left_operand, right_operand):
        self.operands = [left_operand, right_operand]
        self.left_operand = left_operand
        self.right_operand = right_operand

    def flatten(self):
        """
            Simplify nested structure of same types
            AND(A, AND(B, AND(C, D))) => AND(A, B, C)
        """
        to_remove = []
        for elem in self.operands:
            # if element belong to same class (nested And's, Or's)
            if isinstance(elem, self.__class__):
                # recursive flattening first
                elem.flatten()
                # remove from current list
                to_remove.append(elem)

        # add new elements
        for elem in to_remove:
            self.operands.remove(elem)
            self.operands.extend(elem.operands)


    def __str__(self):
        content = "("
        for elem in self.operands[:-1]:
            content += f"{elem}, "
        content += f"{self.operands[-1]})"
        return content
        # return (f"({self.left_operand}, {self.right_operand})")


class And(Operator):
    def resolve_to_true(self):
        """
            Check if the different operands resolve to True
            A & B & C = True => AND(A, B, C) = True 
        """
        for elem in self.operands:
            print(f"Checking elem {elem}")
            if not elem.resolve_to_true():
                return False
        return True

    def __str__(self):
        content = super().__str__()
        return "AND" + content


class Or(Operator):

    def resolve_to_true(self):
        """
            Check if the different operands resolve to True
            A | B | C = True => OR(A, B, C) = True 
        """
        for elem in self.operands:
            if elem.resolve_to_true():
                return True
        return False

    def __str__(self):
        content = super().__str__()
        return "OR" + content


class Xor(Operator):

    def resolve_to_true(self):
        # How Reduce works ?
        # for array [a, b, c, d, e]
        # return a ^ b ^ c ^ d ^ e
        resolved = list(map(lambda x: x.resolve_to_true(), self.operands))
        return reduce(lambda x, y: x ^ y, resolved)

    def __str__(self):
        content = super().__str__()
        return "XOR" + content


class Not(Operator):

    def __init__(self, operand):
        self.operand = operand

    def resolve_to_true(self):
        # return True if operand is False.
        return not self.operand.resolve_to_true()

    def __str__(self):
        return f"NOT({self.operand})"

