from dataclasses import dataclass
from enum import Enum

import plox


class Scanner:
    def __init__(self, source: str):
        self.source: str = source
        self.tokens: list["Token"] = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scan_tokens(self) -> list["Token"]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def scan_token(self):
        c = self.advance()
        match c:
            case "(" | ")" | "{" | "}" | "," | "." | "-" | "+" | ";" | "*" as c:
                self.add_token(TokenType(c))
            case "!":
                self.add_token(
                    TokenType.BANG_EQUAL if self.match("=") else TokenType.BANG
                )
            case "=":
                self.add_token(
                    TokenType.EQUAL_EQUAL if self.match("=") else TokenType.EQUAL
                )
            case "<":
                self.add_token(
                    TokenType.LESS_EQUAL if self.match("=") else TokenType.LESS
                )
            case ">":
                self.add_token(
                    TokenType.GREATER_EQUAL if self.match("=") else TokenType.GREATER
                )
            case "/":
                if self.match("/"):
                    # A comment goes until the end of the line.
                    while self.peek() != "\n" and not self.is_at_end():
                        self.advance()
                elif self.match("*"):
                    # A block comment goes until the closing delimiter
                    level = 1
                    while not self.is_at_end():
                        self.advance()
                        # nested comment open
                        if self.peek() == "/" and self.peek_next() == "*":
                            # skip over
                            self.advance()
                            self.advance()
                            level += 1

                        # nested comment close
                        if self.peek() == "*" and self.peek_next() == "/":
                            self.advance()
                            self.advance()
                            level -= 1

                        if level <= 0:
                            break

                else:
                    self.add_token(TokenType.SLASH)
            case " " | "\r" | "\t":
                pass
            case "\n":
                self.line += 1

            case '"':
                self.string()

            case c if c.isdigit():
                self.number()

            case c if c.isalpha():
                self.identifier()

            case _:
                plox.error(self.line, "Unexpected character.")

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def string(self):
        while self.peek() != '"' and not self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            plox.error(self.line, "Unterminated string.")
            return

        # go over terminating "
        self.advance()
        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TokenType.STRING, value)

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == "." and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()

        self.add_token(TokenType.NUMBER, float(self.source[self.start : self.current]))

    def identifier(self):
        while self.peek().isalnum():
            self.advance()

        text = self.source[self.start : self.current]
        try:
            self.add_token(TokenType(text))
        except ValueError:
            self.add_token(TokenType.IDENTIFIER)

    def add_token(self, type: "TokenType", obj: object | None = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(type, text, obj, self.line))

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def is_at_end(self):
        return self.current >= len(self.source)


@dataclass
class Token:
    type: "TokenType"
    lexeme: str
    literal: object
    line: int


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"
    LEFT_BRACE = "{"
    RIGHT_BRACE = "}"
    COMMA = ","
    DOT = "."
    MINUS = "-"
    PLUS = "+"
    SEMICOLON = ";"
    SLASH = "/"
    STAR = "*"

    # One or two character tokens.
    BANG = "!"
    BANG_EQUAL = "!="
    EQUAL = "="
    EQUAL_EQUAL = "=="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = ">"

    # Literals.
    IDENTIFIER = "identifier"
    STRING = "string"
    NUMBER = "number"

    # Keywords.
    AND = "and"
    CLASS = "class"
    ELSE = "else"
    FALSE = "false"
    FUN = "fun"
    FOR = "for"
    IF = "if"
    NIL = "nil"
    OR = "or"
    PRINT = "print"
    RETURN = "return"
    SUPER = "super"
    THIS = "this"
    TRUE = "true"
    VAR = "var"
    WHILE = "while"

    EOF = "eof"
