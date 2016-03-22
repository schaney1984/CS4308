from LuaInterpreter import Token, TokenType, LexicalException

__author__ = "Steven Chaney"


class LexicalAnalyzer(object):
    tokenList = []

    def __init__(self, filename):
        """
        :param filename: cannot be null
        :raises: FileNotFoundException
        :raises: LexicalException
        :raises: ValueError if filename is null
        """
        if filename is None:
            raise ValueError("null file name argument")
        self.tokenList = []
        lineNumber = 0
        input = open(filename)

        for line in input:
            lineNumber += 1
            self.processLine(line, lineNumber)

        input.close()
        self.tokenList.append(Token(TokenType.EOS_TOK, "EOS", lineNumber, 1))


    def processLine(self, line, lineNumber):
        """
        :param line:
        :param lineNumber:
        :return:
        """
        if line is None:
            raise ValueError("null line argument")
        if lineNumber <= 0:
            raise ValueError("invalid line number argument")
        index = skipWhiteSpace(line, 0)
        while index < len(line):
            lexeme = getLexeme(line, index)
            tokType = getTokenType(lexeme, lineNumber, index + 1)
            self.tokenList.append(Token(tokType, lexeme, lineNumber, index + 1))
            index += len(lexeme)
            index = skipWhiteSpace(line, index)


def getTokenType(self, lexeme, rowNumber, columnNumber):
    """
    :param lexeme:
    :param rowNumber:
    :param columnNumber:
    :return:
    """
    if lexeme is None:
        raise ValueError("invalid string argument")
    tokType = TokenType.EOS_TOK
    if lexeme[0].isdigit():                           #could replace with if lexeme.isdigit() and remove nested if
        if allDigits(self, lexeme):
            tokType = TokenType.LITERAL_INTEGER_TOK
        else:
            raise LexicalException("literal integer expected at row" + rowNumber + " and column " + columnNumber)
    elif lexeme[0].isalpha():
        if len(lexeme) == 1:
            tokType = TokenType.ID_TOK
        elif lexeme == "if":
            tokType = TokenType.IF_TOK
        elif lexeme == "function":
            tokType = TokenType.FUNCTION_TOK
        elif lexeme == "then":
            tokType = TokenType.THEN_TOK
        elif lexeme == "end":
            tokType = TokenType.END_TOK
        elif lexeme == "else":
            tokType = TokenType.ELSE_TOK
        elif lexeme == "while":
            tokType = TokenType.WHILE_TOK
        elif lexeme == "do":
            tokType = TokenType.DO_TOK
        elif lexeme == "print":
            tokType = TokenType.PRINT_TOK
        elif lexeme == "repeat":
            tokType = TokenType.REPEAT_TOK
        elif lexeme == "until":
            tokType = TokenType.UNTIL_TOK
        else:
            raise LexicalException("invalid lexeme at row " + rowNumber + " and column " + columnNumber)
    elif lexeme == "(":
        tokType = TokenType.LEFT_PAREN_TOK
    elif lexeme == ")":
        tokType = TokenType.RIGHT_PAREN_TOK
    elif lexeme == ">=":
        tokType = TokenType.GE_TOK
    elif lexeme == ">":
        tokType = TokenType.GT_TOK
    elif lexeme == "<=":
        tokType = TokenType.LE_TOK
    elif lexeme == "<":
        tokType = TokenType.LT_TOK
    elif lexeme == "==":
        tokType = TokenType.EQ_TOK
    elif lexeme == "~=":
        tokType = TokenType.NE_TOK
    elif lexeme == "+":
        tokType = TokenType.ADD_TOK
    elif lexeme == "-":
        tokType = TokenType.SUB_TOK
    elif lexeme == "*":
        tokType = TokenType.MUL_TOK
    elif lexeme == "/":
        tokType = TokenType.DIV_TOK
    elif lexeme == "=":
        tokType = TokenType.ASSIGN_TOK
    else:
        raise LexicalException("invalid lexeme at row " + rowNumber + " and column " + columnNumber)

    return tokType


# allDigits is unnecessary for Python implementation. See built-in isdigit() function. Left intact for completion.
def allDigits(self, lexeme):
    """
    :param lexeme: cannot be null
    :return: whether all characters in lexeme are digits
    :raises: ValueError if lexeme is null
    """
    # if lexeme is None:
    #    raise ValueError("null string argument")
    # i = 0
    # while i < len(lexeme) and lexeme[i].isdigit():
    #    i += 1
    # return i == len(lexeme)
    return lexeme.isdigit()


def getLexeme(self, line, index):
    """
    :param line: cannot be null
    :param index: >= 0
    :return: next lexeme
    :raises: ValueError if line is null or line < 0
    """
    if line is None:
        raise ValueError("null string argument")
    if index < 0:
        raise ValueError("invalid index argument")
    i = index
    while i < len(line) and not line[i].isspace():
        i += 1
    return line[index:i]


def skipWhiteSpace(self, line, index):
    """
    :param line:
    :param index:
    :return: index of the first non whitespace character following position index
    """
    while index < len(line) and line[index].isspace():
        index += 1
    return index


def getLookaheadToken(self):
    """
    :return: copy of the next token
    :raises: LexicalException if there is not another token
    """
    if not self.tokenList:
        raise LexicalException("no more tokens")
    return self.tokenList.get(0)


def getNextToken(self):
    """
    :return: next token (token is removed)
    :raises: LexicalException if there is not another token
    """
    if not self.tokenList:
        raise LexicalException("no more tokens")
    return self.tokenList.remove(0)