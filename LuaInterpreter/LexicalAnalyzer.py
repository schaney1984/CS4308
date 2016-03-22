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
        self.tokenList.append(Token.Token(TokenType.TokenType.EOS_TOK, "EOS", lineNumber, 1))

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
        index = self.skipWhiteSpace(line, 0)
        while index < len(line):
            lexeme = self.getLexeme(line, index)
            tokType = self.getTokenType(lexeme, lineNumber, index + 1)
            self.tokenList.append(Token.Token(tokType, lexeme, lineNumber, index + 1))
            index += len(lexeme)
            index = self.skipWhiteSpace(line, index)

    def getTokenType(self, lexeme, rowNumber, columnNumber):
        """
        :param lexeme:
        :param rowNumber:
        :param columnNumber:
        :return:
        """
        if lexeme is None:
            raise ValueError("invalid string argument")
        tokType = TokenType.TokenType.EOS_TOK
        if lexeme[0].isdigit():                           #could replace with if lexeme.isdigit() and remove nested if
            if self.allDigits(lexeme):
                tokType = TokenType.TokenType.LITERAL_INTEGER_TOK
            else:
                raise LexicalException.LexicalException("literal integer expected at row" + rowNumber + " and column " + columnNumber)
        elif lexeme[0].isalpha():
            if len(lexeme) == 1:
                tokType = TokenType.TokenType.ID_TOK
            elif lexeme == "if":
                tokType = TokenType.TokenType.IF_TOK
            elif lexeme == "function":
                tokType = TokenType.TokenType.FUNCTION_TOK
            elif lexeme == "then":
                tokType = TokenType.TokenType.THEN_TOK
            elif lexeme == "end":
                tokType = TokenType.TokenType.END_TOK
            elif lexeme == "else":
                tokType = TokenType.TokenType.ELSE_TOK
            elif lexeme == "while":
                tokType = TokenType.TokenType.WHILE_TOK
            elif lexeme == "do":
                tokType = TokenType.TokenType.DO_TOK
            elif lexeme == "print":
                tokType = TokenType.TokenType.PRINT_TOK
            elif lexeme == "repeat":
                tokType = TokenType.TokenType.REPEAT_TOK
            elif lexeme == "until":
                tokType = TokenType.TokenType.UNTIL_TOK
            else:
                raise LexicalException.LexicalException("invalid lexeme at row " + rowNumber + " and column " + columnNumber)
        elif lexeme == "(":
            tokType = TokenType.TokenType.LEFT_PAREN_TOK
        elif lexeme == ")":
            tokType = TokenType.TokenType.RIGHT_PAREN_TOK
        elif lexeme == ">=":
            tokType = TokenType.TokenType.GE_TOK
        elif lexeme == ">":
            tokType = TokenType.TokenType.GT_TOK
        elif lexeme == "<=":
            tokType = TokenType.TokenType.LE_TOK
        elif lexeme == "<":
            tokType = TokenType.TokenType.LT_TOK
        elif lexeme == "==":
            tokType = TokenType.TokenType.EQ_TOK
        elif lexeme == "~=":
            tokType = TokenType.TokenType.NE_TOK
        elif lexeme == "+":
            tokType = TokenType.TokenType.ADD_TOK
        elif lexeme == "-":
            tokType = TokenType.TokenType.SUB_TOK
        elif lexeme == "*":
            tokType = TokenType.TokenType.MUL_TOK
        elif lexeme == "/":
            tokType = TokenType.TokenType.DIV_TOK
        elif lexeme == "=":
            tokType = TokenType.TokenType.ASSIGN_TOK
        else:
            raise LexicalException.LexicalException("invalid lexeme at row " + rowNumber + " and column " + columnNumber)

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
            raise LexicalException.LexicalException("no more tokens")
        return self.tokenList[0]

    def getNextToken(self):
        """
        :return: next token (token is removed)
        :raises: LexicalException if there is not another token
        """
        if not self.tokenList:
            raise LexicalException.LexicalException("no more tokens")
        return self.tokenList.remove(0)