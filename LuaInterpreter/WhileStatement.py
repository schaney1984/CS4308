__author__ = "Steven Chaney"


class WhileStatement(object):
    def __init__(self, expr, blk):
        """
        :param expr: cannot be null
        :param blk: cannot be null
        :raises: ValueError if either argument is null
        """
        if expr is None:
            raise ValueError("null boolean expression argument")
        if blk is None:
            raise ValueError("null block argument")
        self.expr = expr
        self.blk = blk

    def execute(self):
        while self.expr.evaluate():
            self.blk.execute()
