from LuaInterpreter import Memory, Id, ArithmeticExpression

__author__ = "Steven Chaney"


class AssignmentStatement(object):
    var = Id()
    expr = ArithmeticExpression()

    def __init__(self, var, expr):
        """
        :param var: cannot be null
        :param expr: cannot be null
        :raises: ValueError if either var or expr is null
        """
        if var is None:
            raise ValueError("null Id argument")
        if expr is None:
            raise ValueError("null ArithmeticExpression argument")
        self.var = var
        self.expr = expr

    def execute(self):
        Memory.store(self.var.getChar(), self.expr.evaluate())
