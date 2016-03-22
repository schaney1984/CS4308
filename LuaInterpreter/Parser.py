from LuaInterpreter import LexicalAnalyzer, LexicalException, ParserException, TokenType, BooleanExpression, Id,\
     LiteralInteger, BinaryExpression, IfStatement, WhileStatement, PrintStatement, RepeatStatement, Statement, Token,\
     AssignmentStatement, Block, Program

__author__ = "Steven Chaney"

# Parser class implements a recursive descent parsing algorithm
# for the given g rammar of a subset of Lua


class Parser(object):

    def __init__(self, filename):
        """
        :param filename:  cannot be null - checked in LexicalAnalyzer
        :raises: FileNotFound exception if file cannot be found
        :raises: LexicalException
        :postcondition: parser object has been created
        """
        self.lex = LexicalAnalyzer(filename)

    def parse(self):
        """
        :return: Program object containing an intermediate representation of the program
        :raises: ParserException if a parsing error occurred
        implements the production <program> -> function id() <block> end
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.FUNCTION_TOK)
        functionName = self.getId()
        tok = self.getNextToken()
        self.match(tok, TokenType.LEFT_PAREN_TOK)
        tok = self.getNextToken()
        self.match(tok, TokenType.RIGHT_PAREN_TOK)
        blk = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.END_TOK)
        tok = self.getNextToken()
        if tok.getTokType() is not TokenType.EOS_TOK:
            raise ParserException("garbage at end of file")
        return Program(blk)

    def getBlock(self):
        """
        :return: Block object
        :raises: ParserException if a parsing error occurred
        implements the production <block> -> <statement> | <statement> <block>
        """
        blk = Block()
        tok = self.getLookaheadToken()
        while self.isValidStartOfStatement(tok):
            stmt = self.getStatement()
            blk.add(stmt)
            tok = self.getLookaheadToken()
        return blk

    def getStatement(self):
        """
        :return: Statement object
        :raises: ParserException if a parsing error occurred
        implements the production <statement> -> <if_statement> | <assignment_statement> | <while_statement>
                                                | <print_statement> | <repeat statement>
        """
        tok = self.getLookaheadToken()
        if tok.getTokType() == TokenType.IF_TOK:
            stmt = self.getIfStatement()
        elif tok.getTokType() == TokenType.WHILE_TOK:
            stmt = self.getWhileStatement()
        elif tok.getTokType() == TokenType.PRINT_TOK:
            stmt = self.getPrintStatement()
        elif tok.getTokType() == TokenType.REPEAT_TOK:
            stmt = self.getRepeatStatement()
        elif tok.getTokType() == TokenType.ID_TOK:
            stmt = self.getAssignmentStatement()
        else:
            raise ParserException("invalid statement at row " + tok.getRowNumber() +
                                  " and column " + tok.getColumnNumber())
        return stmt

    def getAssignmentStatement(self):
        """
        :return: assignment statement
        :raises: ParserException if a parsing error occurred
        implements the production <assignment_statement> -> id <assignment_operator> <arithmetic_expression>
        """
        var = self.getId()
        tok = self.getNextToken()
        self.match(tok, TokenType.ASSIGN_TOK)
        expr = self.getArithmeticExpression()
        return AssignmentStatement(var, expr)

    def getRepeatStatement(self):
        """
        :return: repeat statement
        :raises: ParserException if a parsing error occurred
        implements the production <repeat_statement> -> repeat <block> until <boolean_expression>
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.REPEAT_TOK)
        blk = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.UNTIL_TOK)
        expr = self.getBooleanExpression()
        return RepeatStatement(blk, expr)

    def getPrintStatement(self):
        """
        :return: print statement
        :raises: ParserException if a parsing error occurred
        implements the production <print_statement> -> print ( <arithmetic_expression )
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.PRINT_TOK)
        tok = self.getNextToken()
        self.match(tok, TokenType.LEFT_PAREN_TOK)
        expr = self.getArithmeticExpression()
        tok = self.getNextToken()
        self.match(tok, TokenType.RIGHT_PAREN_TOK)
        return PrintStatement(expr)

    def getWhileStatement(self):
        """
        :return: while statement
        :raises: ParserException if a parsing error occurred
        implements the production <while_statement> -> while <boolean_expression> do <block> end
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.WHILE_TOK)
        expr = self.getBooleanExpression()
        tok = self.getNextToken()
        self.match(tok, TokenType.DO_TOK)
        blk = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.END_TOK)
        return WhileStatement(expr, blk)

    def getIfStatement(self):
        """
        :return: if statement
        :raises: ParserException if a parsing error occurred
        implements the production <if_statement> -> if <boolean_expression> then <block> else <block> end
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.IF_TOK)
        expr = self.getBooleanExpression()
        tok = self.getNextToken()
        self.match(tok, TokenType.THEN_TOK)
        blk1 = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.ELSE_TOK)
        blk2 = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.END_TOK)
        return IfStatement(expr, blk1, blk2)

    def isValidStartOfStatement(self, tok):
        """
        :param tok: cannot be null -- checked with assertion
        :return: whether tok can be the start of a statement
        """
        assert tok is not None
        return tok.getTokType() == TokenType.ID_TOK or\
            tok.getTokType() == TokenType.IF_TOK or\
            tok.getTokType() == TokenType.WHILE_TOK or\
            tok.getTokType() == TokenType.PRINT_TOK or\
            tok.getTokType() == TokenType.REPEAT_TOK

    def getArithmeticExpression(self):
        """
        :return: arithmetic expression
        :raises: ParserException if a parsing error occurred
        implements the production <arithmetic_expression> -> <id> | <literal_integer>
                                    | <arithmetic_op> <arithmetic_expression> <arithmetic_expression>
        """
        tok = self.getLookaheadToken()
        if tok.getTokType() == TokenType.ID_TOK:
            expr = self.getId()
        elif tok.getTokType() == TokenType.LITERAL_INTEGER_TOK:
            expr = self.getLiteralInteger()
        else:
            expr = self.getBinaryExpression()
        return expr

    def getBinaryExpression(self):
        """
        :return: binary expression
        :raises: ParserException if a parsing error occurred
        implements the grammar expression <arithmetic_op> <arithmetic_expression> <arithmetic_expression>
        """
        op = self.getArithmeticOperator()
        expr1 = self.getArithmeticExpression()
        expr2 = self.getArithmeticExpression()
        return BinaryExpression(op, expr1, expr2)

    def getArithmeticOperator(self):
        """
        :return: arithmetic operator
        :raises: ParserException if a parsing error occurred
        implements the production <arithmetic_op> -> add_operator | sub_operator | mul_operator | div_operator
        """
        tok = self.getNextToken()
        if tok.getTokType() == TokenType.ADD_TOK:
            op = BinaryExpression.ArithmeticOperator.ADD_OP
        elif tok.getTokType() == TokenType.SUB_TOK:
            op = BinaryExpression.ArithmeticOperator.SUB_OP
        elif tok.getTokType() == TokenType.MUL_TOK:
            op = BinaryExpression.ArithmeticOperator.MUL_OP
        elif tok.getTokType() == TokenType.DIV_TOK:
            op = BinaryExpression.ArithmeticOperator.DIV_OP
        else:
            raise ParserException("arithmetic operator expected at row " + tok.getRowNumber() +
                                  " and column " + tok.getColumnNumber())
        return op

    def getLiteralInteger(self):
        """
        :return: literal integer
        :raises: ParserException if a parsing error occurred
        """
        tok = self.getNextToken()
        if tok.getTokType() is not TokenType.LITERAL_INTEGER_TOK:
            raise ParserException("literal integer expected at row " + tok.getRowNumber() +
                                  " and column " + tok.getColumnNumber())
        try:
            value = int(tok.getLexeme())
        except ValueError:
            print("ValueError: int expected at row " + tok.getRowNumber() + " and column " + tok.getColumnNumber())
        return LiteralInteger(value)

    def getId(self):
        """
        :return: an id
        :raises: ParserException if a parsing error occurred
        """
        tok = self.getNextToken()
        if tok.getTokType is not TokenType.ID_TOK:
            raise ParserException("identifier expected at row " + tok.getRowNumber() +
                                  " and column " + tok.getColumnNumber())
        return Id(tok.getLexeme()[0])

    def getBooleanExpression(self):
        """
        :return: boolean expression
        :raises: ParserException if a parsing error occurred
        implements the production <boolean_expression> -> <relative_op> <arithmetic_expression> <arithmetic_expression>
        """
        op = self.getRelationalOperator()
        expr1 = self.getArithmeticExpression()
        expr2 = self.getArithmeticExpression()
        return BooleanExpression(op, expr1, expr2)

    def getRelationalOperator(self):
        """
        :return: relative operator
        :raises: ParserException if a parsing error occurred
        implements the production <relative_op> → le_operator | lt_operator | ge_operator | gt_operator | eq_operator | ne_operator
        """
        tok = self.getNextToken()
        if tok.getTokType() == TokenType.EQ_TOK:
            op = BooleanExpression.RelationalOperator.EQ_OP
        elif tok.getTokType() == TokenType.NE_TOK:
            op = BooleanExpression.RelationalOperator.NE_OP
        elif tok.getTokType() == TokenType.GT_OP:
            op = BooleanExpression.RelationalOperator.GT_OP
        elif tok.getTokType() == TokenType.GE_OP:
            op = BooleanExpression.RelationalOperator.GE_OP
        elif tok.getTokType() == TokenType.LT_OP:
            op = BooleanExpression.RelationalOperator.LT_OP
        elif tok.getTokType() == TokenType.LE_OP:
            op = BooleanExpression.RelationalOperator.LE_OP
        else:
            raise ParserException("relational operator expected at row" + tok.getRowNumber() +
                                  " and column " + tok.getColumnNumber())
        return op

    def match(self, tok, tokType):
        """
        :param tok: cannot be null -- checked by assertion
        :param tokType: cannot be null -- checked by assertion
        :raises: ParserException if type of tok is not tokType
        """
        assert tok is not None
        assert tokType is not None
        if tok.getTokType is not tokType:
            raise ParserException(tokType + " expected at row " + tok.getRowNumber() +
                                  " and column " + tok.getColumnNumber())


    def getLookaheadToken(self):
        """
        :return: copy of next token
        :raises: ParserException if there are no more tokens
        """
        try:
            tok = self.lex.getLookaheadToken()
        except LexicalException:
            raise ParserException("no more tokens")
        return tok

    def getNextToken(self):
        """
        :return: next token
        :raises: ParserException if there are no more tokens
        """
        try:
            tok = self.lex.getNextToken()
        except LexicalException:
            raise ParserException("no more tokens")
        return tok
