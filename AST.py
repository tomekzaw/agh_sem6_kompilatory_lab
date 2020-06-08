from dataclasses import dataclass
from typing import Any
from scanner import lexer


@dataclass
class Node(object):
    def __new__(cls, *args, **kwargs):
        obj = object.__new__(cls)
        obj.lineno = lexer.lineno
        return obj

    def accept(self, visitor):
        return visitor.visit(self)

    # @property
    # def children(self):
    #     return self.__dict__.values()


@dataclass
class Program(Node):
    instructions: Any


@dataclass
class Instructions(Node):
    instructions: Any


# @dataclass
# class EmptyInstruction(Node):
#     pass


@dataclass
class If(Node):
    condition: Any
    instruction_then: Any
    instruction_else: Any = None


@dataclass
class For(Node):
    variable: Any
    range_: Any
    instruction: Any


@dataclass
class Range(Node):
    start: Any
    end: Any


@dataclass
class While(Node):
    condition: Any
    instruction: Any


@dataclass
class Condition(Node):
    op: Any
    left: Any
    right: Any


@dataclass
class Break(Node):
    pass


@dataclass
class Continue(Node):
    pass


@dataclass
class Return(Node):
    value: Any = None


@dataclass
class Print(Node):
    args: Any


@dataclass
class Assignment(Node):
    op: Any
    left: Any
    right: Any


@dataclass
class Variable(Node):
    name: Any


@dataclass
class Reference(Node):
    variable: Any
    indices: Any


@dataclass
class BinExpr(Node):
    op: Any
    left: Any
    right: Any


@dataclass
class UnaryExpr(Node):
    op: Any
    expr: Any


@dataclass
class Constant(Node):
    value: Any


@dataclass
class IntNum(Constant):
    pass


@dataclass
class FloatNum(Constant):
    pass


@dataclass
class String(Constant):
    pass


# @dataclass
# class Matrix(Node):
#     rows: list


@dataclass
class Vector(Node):
    elements: list


@dataclass
class MatrixSpecialFunction(Node):
    rows: Any
    cols: Any = None


@dataclass
class Eye(MatrixSpecialFunction):
    pass


@dataclass
class Zeros(MatrixSpecialFunction):
    pass


@dataclass
class Ones(MatrixSpecialFunction):
    pass


@dataclass
class Error(Node):
    pass
