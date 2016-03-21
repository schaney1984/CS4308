from LuaInterpreter import Token, TokenType


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
        while(index < len(line)):
            lexeme = getLexeme(line, index)
            tokType = getTokenType(lexeme, lineNumber, index + 1)
            self.tokenList.append(Token(tokType, lexeme, lineNumber, index + 1))
            index += len(lexeme)
            index = skipWhiteSpace(line, index)
