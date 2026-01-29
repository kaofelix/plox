from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatch

from plox.expr import Expr
from plox.scanner import Token, TokenType


class Stmt(ABC):
    pass


@dataclass
class Expression(Stmt):
    expression: Expr


@dataclass
class Print(Stmt):
    expression: Expr
