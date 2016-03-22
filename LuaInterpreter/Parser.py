from LuaInterpreter import LexicalAnalyzer, LexicalException, ParserException, TokenType, BooleanExpression, Id, \
    LiteralInteger, BinaryExpression, IfStatement, WhileStatement, PrintStatement, RepeatStatement, \
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
        self.lex = LexicalAnalyzer.LexicalAnalyzer(filename)

    def parse(self):
        """
        :return: Program object containing an intermediate representation of the program
        :raises: ParserException if a parsing error occurred
        implements the production <program> -> function id() <block> end
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.FUNCTION_TOK)
#        functionName = self.getId()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.LEFT_PAREN_TOK)
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.RIGHT_PAREN_TOK)
        blk = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.END_TOK)
        tok = self.getNextToken()
        if tok.getTokType() is not TokenType.TokenType.EOS_TOK:
            raise ParserException.ParserException("garbage at end of file")
        return Program.Program(blk)

    def getBlock(self):
        """
        :return: Block object
        :raises: ParserException if a parsing error occurred
        implements the production <block> -> <statement> | <statement> <block>
        """
        blk = Block.Block()
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
        if tok.getTokType() == TokenType.TokenType.IF_TOK:
            stmt = self.getIfStatement()
        elif tok.getTokType() == TokenType.TokenType.WHILE_TOK:
            stmt = self.getWhileStatement()
        elif tok.getTokType() == TokenType.TokenType.PRINT_TOK:
            stmt = self.getPrintStatement()
        elif tok.getTokType() == TokenType.TokenType.REPEAT_TOK:
            stmt = self.getRepeatStatement()
        elif tok.getTokType() == TokenType.TokenType.ID_TOK:
            stmt = self.getAssignmentStatement()
        else:
            raise ParserException.ParserException("invalid statement at row " + str(tok.getRowNumber()) +
                                                  " and column " + str(tok.getColumnNumber()))
        return stmt

    def getAssignmentStatement(self):
        """
        :return: assignment statement
        :raises: ParserException if a parsing error occurred
        implements the production <assignment_statement> -> id <assignment_operator> <arithmetic_expression>
        """
        var = self.getId()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.ASSIGN_TOK)
        expr = self.getArithmeticExpression()
        return AssignmentStatement.AssignmentStatement(var, expr)

    def getRepeatStatement(self):
        """
        :return: repeat statement
        :raises: ParserException if a parsing error occurred
        implements the production <repeat_statement> -> repeat <block> until <boolean_expression>
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.REPEAT_TOK)
        blk = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.UNTIL_TOK)
        expr = self.getBooleanExpression()
        return RepeatStatement.RepeatStatement(blk, expr)

    def getPrintStatement(self):
        """
        :return: print statement
        :raises: ParserException if a parsing error occurred
        implements the production <print_statement> -> print ( <arithmetic_expression )
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.PRINT_TOK)
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.LEFT_PAREN_TOK)
        expr = self.getArithmeticExpression()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.RIGHT_PAREN_TOK)
        return PrintStatement.PrintStatement(expr)

    def getWhileStatement(self):
        """
        :return: while statement
        :raises: ParserException if a parsing error occurred
        implements the production <while_statement> -> while <boolean_expression> do <block> end
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.WHILE_TOK)
        expr = self.getBooleanExpression()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.DO_TOK)
        blk = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.END_TOK)
        return WhileStatement.WhileStatement(expr, blk)

    def getIfStatement(self):
        """
        :return: if statement
        :raises: ParserException if a parsing error occurred
        implements the production <if_statement> -> if <boolean_expression> then <block> else <block> end
        """
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.IF_TOK)
        expr = self.getBooleanExpression()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.THEN_TOK)
        blk1 = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.ELSE_TOK)
        blk2 = self.getBlock()
        tok = self.getNextToken()
        self.match(tok, TokenType.TokenType.END_TOK)
        return IfStatement.IfStatement(expr, blk1, blk2)

    def isValidStartOfStatement(self, tok):
        """
        :param tok: cannot be null -- checked with assertion
        :return: whether tok can be the start of a statement
        """
        assert tok is not None
        return tok.getTokType() == TokenType.TokenType.ID_TOK or \
               tok.getTokType() == TokenType.TokenType.IF_TOK or \
               tok.getTokType() == TokenType.TokenType.WHILE_TOK or \
               tok.getTokType() == TokenType.TokenType.PRINT_TOK or \
               tok.getTokType() == TokenType.TokenType.REPEAT_TOK

    def getArithmeticExpression(self):
        """
        :return: arithmetic expression
        :raises: ParserException if a parsing error occurred
        implements the production <arithmetic_expression> -> <id> | <literal_integer>
                                    | <arithmetic_op> <arithmetic_expression> <arithmetic_expression>
        """
        tok = self.getLookaheadToken()
        if tok.getTokType() == TokenType.TokenType.ID_TOK:
            expr = self.getId()
        elif tok.getTokType() == TokenType.TokenType.LITERAL_INTEGER_TOK:
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
        return BinaryExpression.BinaryExpression(op, expr1, expr2)

    def getArithmeticOperator(self):
        """
        :return: arithmetic operator
        :raises: ParserException if a parsing error occurred
        implements the production <arithmetic_op> -> add_operator | sub_operator | mul_operator | div_operator
        """
        tok = self.getNextToken()
        if tok.getTokType() == TokenType.TokenType.ADD_TOK:
            op = BinaryExpression.ArithmeticOperator.ADD_OP
        elif tok.getTokType() == TokenType.TokenType.SUB_TOK:
            op = BinaryExpression.ArithmeticOperator.SUB_OP
        elif tok.getTokType() == TokenType.TokenType.MUL_TOK:
            op = BinaryExpression.ArithmeticOperator.MUL_OP
        elif tok.getTokType() == TokenType.TokenType.DIV_TOK:
            op = BinaryExpression.ArithmeticOperator.DIV_OP
        else:
            raise ParserException.ParserException("arithmetic operator expected at row " + str(tok.getRowNumber()) +
                                                  " and column " + str(tok.getColumnNumber()))
        return op

    def getLiteralInteger(self):
        """
        :return: literal integer
        :raises: ParserException if a parsing error occurred
        """
        tok = self.getNextToken()
        if tok.getTokType() is not TokenType.TokenType.LITERAL_INTEGER_TOK:
            raise ParserException.ParserException("literal integer expected at row " + str(tok.getRowNumber()) +
                                                  " and column " + str(tok.getColumnNumber()))
        value = 0
        try:
            value = int(tok.getLexeme())
        except ValueError:
            print("ValueError: int expected at row " + str(tok.getRowNumber()) + " and column " + str(tok.getColumnNumber()))
        return LiteralInteger.LiteralInteger(value)

    def getId(self):
        """
        :return: an id
        :raises: ParserException if a parsing error occurred
        """
        tok = self.getNextToken()
        if tok.getTokType is not TokenType.TokenType.ID_TOK:
            raise ParserException.ParserException("identifier expected at row " + str(tok.getRowNumber()) +
                                                  " and column " + str(tok.getColumnNumber()))
        return Id.Id(tok.getLexeme()[0])

    def getBooleanExpression(self):
        """
        :return: boolean expression
        :raises: ParserException if a parsing error occurred
        implements the production <boolean_expression> -> <relative_op> <arithmetic_expression> <arithmetic_expression>
        """
        op = self.getRelationalOperator()
        expr1 = self.getArithmeticExpression()
        expr2 = self.getArithmeticExpression()
        return BooleanExpression.BooleanExpression(op, expr1, expr2)

    def getRelationalOperator(self):
        """
        :return: relative operator
        :raises: ParserException if a parsing error occurred
        implements the production <relative_op> → le_operator | lt_operator | ge_operator | gt_operator | eq_operator | ne_operator
        """
        tok = self.getNextToken()
        if tok.getTokType() == TokenType.TokenType.EQ_TOK:
            op = BooleanExpression.RelationalOperator.EQ_OP
        elif tok.getTokType() == TokenType.TokenType.NE_TOK:
            op = BooleanExpression.RelationalOperator.NE_OP
        elif tok.getTokType() == TokenType.TokenType.GT_OP:
            op = BooleanExpression.RelationalOperator.GT_OP
        elif tok.getTokType() == TokenType.TokenType.GE_OP:
            op = BooleanExpression.RelationalOperator.GE_OP
        elif tok.getTokType() == TokenType.TokenType.LT_OP:
            op = BooleanExpression.RelationalOperator.LT_OP
        elif tok.getTokType() == TokenType.TokenType.LE_OP:
            op = BooleanExpression.RelationalOperator.LE_OP
        else:
            raise ParserException.ParserException("relational operator expected at row" + str(tok.getRowNumber()) +
                                                  " and column " + str(tok.getColumnNumber()))
        return op

    def match(self, tok, tokType):
        """
        :param tok: cannot be null -- checked by assertion
        :param tokType: cannot be null -- checked by assertion
        :raises: ParserException if type of tok is not tokType
        """
        assert tok is not None
        assert tokType is not None
        if tok.getTokType() is not tokType:
            raise ParserException.ParserException(str(tokType) + " expected at row " + str(tok.getRowNumber()) +
                                                  " and column " + str(tok.getColumnNumber()))

    def getLookaheadToken(self):
        """
        :return: copy of next token
        :raises: ParserException if there are no more tokens
        """
        try:
            tok = self.lex.getLookaheadToken()
        except LexicalException.LexicalException:
            raise ParserException.ParserException("no more tokens")
        return tok

    def getNextToken(self):
        """
        :return: next token
        :raises: ParserException if there are no more tokens
        """
        try:
            tok = self.lex.getNextToken()
        except LexicalException.LexicalException:
            raise ParserException.ParserException("no more tokens")
        return tok
