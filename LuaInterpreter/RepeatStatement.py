__author__ = "Steven Chaney"


class RepeatStatement(object):
    def __init__(self, blk, expr):
        """
        :param blk: cannot be null
        :param expr: cannot be null
        :raises: ValueError if either parameter is null
        """
        if blk is None:
            raise ValueError("null block argument")
        if expr is None:
            raise ValueError("null boolean expression argument")
        self.blk = blk
        self.expr = expr

    def execute(self):
        self.blk.execute()
        while not self.expr.evaluate():
            self.blk.execute()
