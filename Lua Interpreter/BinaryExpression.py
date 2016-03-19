

class BinaryExpression:
    """
    @param op cannot be None
    @param expr1 cannot be None
    @param expr2 cannot be None
    @raises ValueError if any argument is None
    """
    def __init__(self, op, expr1, expr2):
        if op is None:
            raise ValueError("null arithmetic operator argument")
        if expr1 is None or expr2 is None:
            raise ValueError("null arithmetic expression argument")
        self.op = op
        self.expr1 = expr1
        self.expr2 = expr2

    def evaluate(self):
        value = 0
        return
