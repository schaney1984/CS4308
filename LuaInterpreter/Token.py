__author__ = "Steven Chaney"


class Token(object):
    def __init__(self, tokType, lexeme, rowNumber, columnNumber):
        """
        :param tokType: cannot be null
        :param lexeme: cannot be null & cannot be empty
        :param rowNumber: must be positive
        :param columnNumber: must be positive
        :raises: ValueError if any precondition is not satisfied
        """
        if tokType is None:
            raise ValueError("null TokenType argument")
        if lexeme is None or len(lexeme) == 0:
            raise ValueError("invalid lexeme argument")
        if rowNumber <= 0:
            raise ValueError("invalid row number argument")
        if columnNumber <= 0:
            raise ValueError("invalid column number argument")

        self.tokType = tokType
        self.lexeme = lexeme
        self.rowNumber = rowNumber
        self.columnNumber = columnNumber

    def getTokType(self):
        return self.tokType

    def getLexeme(self):
        return self.lexeme

    def getRowNumber(self):
        return self.rowNumber

    def getColumnNumber(self):
        return self.columnNumber
