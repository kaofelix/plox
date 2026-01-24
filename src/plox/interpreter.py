from abc import ABC, abstractmethod
from asyncio import Protocol
from dataclasses import dataclass
from functools import singledispatch

from plox.expressions import Binary, Expr, Grouping, Literal, Unary
from plox.scanner import Token, TokenType


def interpret(expression: Expr):
    try:
        value = evaluate(expression)
        print(stringfy(value))
    except RuntimeError as error:
        


@singledispatch
def _interpret(expr: Binary):
    left = evaluate(expr.left)
    right = evaluate(expr.right)

    match expr.operator.type:
        case TokenType.GREATER:
            check_number_operands(expr.operator, left, right)
            return float(left) > float(right)
        case TokenType.GREATER_EQUAL:
            check_number_operands(expr.operator, left, right)
            return float(left) >= float(right)
        case TokenType.LESS:
            check_number_operands(expr.operator, left, right)
            return float(left) < float(right)
        case TokenType.LESS_EQUAL:
            check_number_operands(expr.operator, left, right)
            return float(left) <= float(right)

        case TokenType.MINUS:
            check_number_operands(expr.operator, left, right)
            return float(left) - float(right)
        case TokenType.SLASH:
            check_number_operands(expr.operator, left, right)
            return float(left) / float(right)
        case TokenType.STAR:
            check_number_operands(expr.operator, left, right)
            return float(left) * float(right)

        case TokenType.EQUAL:
            return left == right
        case TokenType.BANG_EQUAL:
            return not (left == right)

        case TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)
            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)
            raise RuntimeError(expr.operator, "Operands must be both string or numbers")


@_interpret.register
def _(expr: Grouping):
    return evaluate(expr.expression)


@_interpret.register
def _(expr: Literal):
    return expr.value


@_interpret.register
def _(expr: Unary):
    right = evaluate(expr.right)

    match expr.operator.type:
        case TokenType.MINUS:
            check_number_operand(expr.operator, right)
            return -float(right)
        case TokenType.BANG:
            return not is_truthy(right)


def evaluate(expr: Expr):
    return _interpret(expr)


def is_truthy(obj: object):
    if obj is None:
        return False

    if isinstance(obj, bool):
        return obj

    return True


def check_number_operand(operator: Token, operand: object):
    if isinstance(operand, float):
        return

    raise RuntimeError(operator, "Operand must be numbers.")


def check_number_operands(operator: Token, left: object, right: object):
    if isinstance(left, float) and isinstance(right, float):
        return

    raise RuntimeError(operator, "Operands must be numbers.")


def stringfy(value: object):
    if object is None: return "nil"
    return str(object)

if __name__ == "__main__":
    a = Literal(value=123)
    plus = Token(TokenType.PLUS, lexeme="+", literal="+", line=1)
    b = Literal(value=432)
    print(_interpret(Binary(left=a, operator=plus, right=b)))
