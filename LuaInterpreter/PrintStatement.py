__author__ = "Steven Chaney"


class PrintStatement(object):
    def __init__(self, expr):
        """
        :param expr: cannot be null
        :raises: ValueError if expr is null
        """
        if expr is None:
            raise ValueError("null arithmetic expression argument")
        self.expr = expr

    def execute(self):
        print(self.expr.evaluate())
