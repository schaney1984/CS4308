import abc


class ArithmeticExpression( object ):
    """
    @return value of the arithmetic expression
    """

    @abc.abstractmethod
    def evaluate(self):
        return
