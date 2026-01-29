import plox
from plox import expr, stmt
from plox.scanner import Token, TokenType


class ParserError(RuntimeError):
    pass


class Parser:
    def __init__(self, tokens: list[Token]):
        self.current = 0
        self.tokens = tokens

    def parse(self) -> list[stmt.Stmt]:
        statements = []
        while not self.is_at_end():
            statements.append(self.statement())

        return statements

    def statement(self) -> stmt.Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()

        return self.expression_statement()

    def print_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Print(value)

    def expression_statement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return stmt.Expression(value)

    def expression(self):
        return self.equality()

    def equality(self):
        expression = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expression = expr.Binary(expression, operator, right)

        return expression

    def comparison(self):
        expression = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS,
            TokenType.LESS_EQUAL,
        ):
            operator = self.previous()
            right = self.term()
            expression = expr.Binary(expression, operator, right)

        return expression

    def term(self):
        expression = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expression = expr.Binary(expression, operator, right)

        return expression

    def factor(self):
        expression = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expression = expr.Binary(expression, operator, right)

        return expression

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return expr.Unary(operator, right)

        return self.primary()

    def primary(self):
        if self.match(TokenType.FALSE):
            return expr.Literal(False)
        if self.match(TokenType.TRUE):
            return expr.Literal(True)
        if self.match(TokenType.NIL):
            return expr.Literal(None)

        if self.match(TokenType.NUMBER, TokenType.STRING):
            return expr.Literal(self.previous().literal)

        if self.match(TokenType.LEFT_PAREN):
            expression = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return expr.Grouping(expression)

        raise self.error(self.peek(), "Expect expression.")

    def match(self, *types: TokenType):
        for type_ in types:
            if self.check(type_):
                self.advance()
                return True

        return False

    def check(self, type_: TokenType):
        if self.is_at_end():
            return False

        return self.peek().type == type_

    def advance(self):
        if not self.is_at_end():
            self.current += 1

        return self.previous()

    def is_at_end(self):
        return self.peek().type == TokenType.EOF

    def peek(self) -> Token:
        return self.tokens[self.current]

    def previous(self) -> Token:
        return self.tokens[self.current - 1]

    def consume(self, type_: TokenType, message: str):
        if self.check(type_):
            return self.advance()

        raise self.error(self.peek(), message)

    def error(self, token: Token, message: str):
        plox.error(token, message)
        return ParserError()

    def synchronize(self):
        self.advance()

        while not self.is_at_end():
            if self.previous().type == TokenType.SEMICOLON:
                return

            match self.peek().type:
                case (
                    TokenType.CLASS
                    | TokenType.FUN
                    | TokenType.VAR
                    | TokenType.FOR
                    | TokenType.IF
                    | TokenType.WHILE
                    | TokenType.PRINT
                    | TokenType.RETURN
                ):
                    return

            self.advance()
