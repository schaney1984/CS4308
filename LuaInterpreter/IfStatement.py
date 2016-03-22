from LuaInterpreter import BooleanExpression, Block

__author__ = "Steven Chaney"


class IfStatement(object):

    expr = BooleanExpression()
    blk1 = Block()
    blk2 = Block()

    def __init__(self, expr, blk1, blk2):
        """
        :param expr: cannot be null
        :param blk1: cannot be null
        :param blk2: cannot be null
        :raises: ValueError if any argument is null
        """
        if expr is None:
            raise ValueError("null boolean expression argument")
        if blk1 is None or blk2 is None:
            raise ValueError("null block argument")
        self.expr = expr
        self.blk1 = blk1
        self.blk2 = blk2

    def execute(self):
        if self.expr.evaluate():
            self.blk1.execute()
        else:
            self.blk2.execute()
