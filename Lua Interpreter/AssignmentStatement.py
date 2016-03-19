

class AssignmentStatement(object):
    """
    @param id cannot be None
    @param expr cannot be None
    @raises ValueError if either id or expr is None
    """
    def __init__(self, id, expr):
        if id is None:
            raise ValueError("null Id argument")
        if expr is None:
            raise ValueError("null ArithmeticExpression argument")
        self.Id = id
        self.ArithmeticExpression = expr

    def execute(self):
        pass
