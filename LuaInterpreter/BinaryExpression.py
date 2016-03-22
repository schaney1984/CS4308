from enum import Enum

__author__ = "Steven Chaney"


class ArithmeticOperator(Enum):
        ADD_OP = 0
        SUB_OP = 1
        MUL_OP = 2
        DIV_OP = 3


class BinaryExpression:
    def __init__(self, op, expr1, expr2):
        """
        :param op: cannot be null
        :param expr1: cannot be null
        :param expr2: cannot be null
        :raises: ValueError if any argument is null
        """
        if op is None:
            raise ValueError("null arithmetic operator argument")
        if expr1 is None or expr2 is None:
            raise ValueError("null arithmetic expression argument")
        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2

    def evaluate(self):
        """ :return: value of value """
        value = 0
        if self.op == ArithmeticOperator.ADD_OP:
            value = self.expr1.evaluate() + self.expr2.evaluate()
        elif self.op == ArithmeticOperator.SUB_OP:
            value = self.expr1.evaluate() - self.expr2.evaluate()
        elif self.op == ArithmeticOperator.MUL_OP:
            value = self.expr1.evaluate() * self.expr2.evaluate()
        elif self.op == ArithmeticOperator.DIV_OP:
            value = self.expr1.evaluate() / self.expr2.evaluate()
        return value
