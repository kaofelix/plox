from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatch

from plox.expr import Expr
from plox.scanner import Token


class Stmt(ABC):
    pass


@dataclass
class Expression(Stmt):
    expression: Expr


@dataclass
class Print(Stmt):
    expression: Expr


@dataclass
class Var(Stmt):
    name: Token
    initializer: Expr | None


@dataclass
class Block(Stmt):
    statements: list[Stmt]
