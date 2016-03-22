from enum import Enum
from LuaInterpreter import ArithmeticExpression

__author__ = "Steven Chaney"


class RelationalOperator(Enum):
    EQ_OP = 0
    NE_OP = 1
    GT_OP = 2
    GE_OP = 3
    LT_OP = 4
    LE_OP = 5


class BooleanExpression(object):
    op = RelationalOperator()
    expr1 = ArithmeticExpression()
    expr2 = ArithmeticExpression()

    def __init__(self, op, expr1, expr2):
        """
        :param op: cannot be null
        :param expr1: cannot be null
        :param expr2: cannot be null
        :raises: ValueError if any argument is None
        """
        if op is None:
            raise ValueError("null relational operator argument")
        if expr1 is None or expr2 is None:
            raise ValueError("null arithmetic expression argument")

        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2

    def evaluate(self):
        """
        :return: value of the boolean expression
        """
        result = False
        if self.op == RelationalOperator.EQ_OP:
            result = self.expr1.evaluate() == self.expr2.evaluate()
        elif self.op == RelationalOperator.NE_OP:
            result = self.expr1.evaluate() != self.expr2.evaluate()
        elif self.op == RelationalOperator.LT_OP:
            result = self.expr1.evaluate() < self.expr2.evaluate()
        elif self.op == RelationalOperator.LE_OP:
            result = self.expr1.evaluate() <= self.expr2.evaluate()
        elif self.op == RelationalOperator.GT_OP:
            result = self.expr1.evaluate() > self.expr2.evaluate()
        elif self.op == RelationalOperator.GE_OP:
            result = self.expr1.evaluate() >= self.expr2.evaluate()

        return result
