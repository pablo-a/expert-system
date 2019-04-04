from functools import reduce
from termcolor import colored


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
        print(colored(f"Checking {self}\n", attrs=['bold', 'underline']))
        for elem in self.operands:
            # print(f"Checking elem {elem}")
            if not elem.resolve_to_true():
                print(colored(f"Since {elem} is False then {self} is False\n", attrs=[
                      'bold', 'underline']))
                return False
        print(colored(f"{self} is True !\n", attrs=['bold', 'underline']))
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
        print(colored(f"Checking {self}\n", attrs=['bold', 'underline']))
        for elem in self.operands:
            if elem.resolve_to_true():
                print(colored(f"Since {elem} is True then {self} is True\n", attrs=[
                      'bold', 'underline']))
                return True
        print(colored(f"Since no element was True then {self} is False\n", attrs=[
              'bold', 'underline']))
        return False

    def __str__(self):
        content = super().__str__()
        return "OR" + content


class Xor(Operator):
    def resolve_to_true(self):
        # How Reduce works ?
        # for array [a, b, c, d, e]
        # return a ^ b ^ c ^ d ^ e
        print(colored(f"Checking {self}\n", attrs=['bold', 'underline']))
        resolved = list(map(lambda x: x.resolve_to_true(), self.operands))
        if reduce(lambda x, y: x ^ y, resolved):
            print(colored(f"{self} is True\n", attrs=['bold', 'underline']))
            return True
        print(colored(f"{self} is False\n", attrs=['bold', 'underline']))
        return False

    def __str__(self):
        content = super().__str__()
        return "XOR" + content


class Not(Operator):
    def __init__(self, operand):
        self.operand = operand

    def resolve_to_true(self):
        # return True if operand is False.
        print(colored(f"Checking {self}\n", "green"))
        if self.operand.resolve_to_true():
            print(colored(f"{self} is False\n", "red"))
            return False
        print(colored(f"{self} is True\n", "red"))
        return True

    def __str__(self):
        return f"NOT({self.operand})"
