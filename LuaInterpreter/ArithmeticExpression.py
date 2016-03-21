import abc


class ArithmeticExpression(object):
    """
    @return value of the arithmetic expression
    """
    def __init__(self):
        pass

    @abc.abstractmethod
    def evaluate(self):
        return
