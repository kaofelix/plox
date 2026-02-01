from abc import ABC, abstractmethod
from ast import stmt
from asyncio import Protocol
from dataclasses import dataclass
from functools import singledispatch

import plox
from plox import expr, stmt
from plox.environment import Environment
from plox.scanner import Token, TokenType

environment = Environment()


def interpret(statements: list[stmt.Stmt]):
    try:
        for statement in statements:
            execute(statement)
    except RuntimeError as error:
        plox.runtime_error(error)


def execute(statement: stmt.Stmt):
    _interpret(statement)


def evaluate(expr: expr.Expr):
    return _interpret(expr)


@singledispatch
def _interpret(binary: expr.Binary):
    left = evaluate(binary.left)
    right = evaluate(binary.right)

    match binary.operator.type:
        case TokenType.GREATER:
            check_number_operands(binary.operator, left, right)
            return float(left) > float(right)
        case TokenType.GREATER_EQUAL:
            check_number_operands(binary.operator, left, right)
            return float(left) >= float(right)
        case TokenType.LESS:
            check_number_operands(binary.operator, left, right)
            return float(left) < float(right)
        case TokenType.LESS_EQUAL:
            check_number_operands(binary.operator, left, right)
            return float(left) <= float(right)

        case TokenType.MINUS:
            check_number_operands(binary.operator, left, right)
            return float(left) - float(right)
        case TokenType.SLASH:
            check_number_operands(binary.operator, left, right)
            return float(left) / float(right)
        case TokenType.STAR:
            check_number_operands(binary.operator, left, right)
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
            raise RuntimeError(
                binary.operator, "Operands must be both string or numbers"
            )


@_interpret.register
def _(grouping: expr.Grouping):
    return evaluate(grouping.expression)


@_interpret.register
def _(literal: expr.Literal):
    return literal.value


@_interpret.register
def _(unary: expr.Unary):
    right = evaluate(unary.right)

    match unary.operator.type:
        case TokenType.MINUS:
            check_number_operand(unary.operator, right)
            return -float(right)
        case TokenType.BANG:
            return not is_truthy(right)


@_interpret.register
def _(variable: expr.Variable):
    return environment.get(variable.name)


@_interpret.register
def _(assignment: expr.Assign):
    value = evaluate(assignment.value)
    environment.assign(assignment.name, value)
    return value


@_interpret.register
def _(expression_statement: stmt.Expression):
    evaluate(expression_statement.expression)


@_interpret.register
def _(print_statement: stmt.Print):
    value = evaluate(print_statement.expression)
    print(stringfy(value))


@_interpret.register
def _(var_declaration: stmt.Var):
    value = None
    if var_declaration.initializer:
        value = evaluate(var_declaration.initializer)

    environment.define(var_declaration.name.lexeme, value)


@_interpret.register
def _(block: stmt.Block):
    execute_block(block.statements, Environment(environment))


def execute_block(statements: list[stmt.Stmt], previous_environment: Environment):
    global environment
    previous_environment = environment
    try:
        environment = previous_environment
        for statement in statements:
            execute(statement)
    finally:
        environment = previous_environment


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
    if value is None:
        return "nil"

    if isinstance(value, float):
        return str(f"{value:g}")

    return str(value)


if __name__ == "__main__":
    a = Literal(value=123)
    plus = Token(TokenType.PLUS, lexeme="+", literal="+", line=1)
    b = Literal(value=432)
    print(_interpret(Binary(left=a, operator=plus, right=b)))
