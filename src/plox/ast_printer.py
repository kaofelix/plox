from abc import ABC, abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from functools import singledispatch

from plox.expressions import Binary, Expr, Grouping, Literal, Unary
from plox.scanner import Token, TokenType


@singledispatch
def ast_printer(expr: Binary):
    return parenthesize(expr.operator.lexeme, expr.left, expr.right)


@ast_printer.register
def _(expr: Grouping):
    return parenthesize("group", expr.expression)


@ast_printer.register
def _(expr: Literal):
    return str(expr.value)


@ast_printer.register
def _(expr: Unary):
    return parenthesize(expr.operator.lexeme, expr.right)


def parenthesize(name: str, *exprs: Expr):
    return f"({name} {' '.join(map(ast_printer, exprs))})"


if __name__ == "__main__":
    a = Literal(value=123)
    plus = Token(TokenType.PLUS, lexeme="+", literal="+", line=1)
    b = Literal(value=432)
    print(ast_printer(Binary(left=a, operator=plus, right=b)))
