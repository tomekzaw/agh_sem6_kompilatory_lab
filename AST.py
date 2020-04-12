from dataclasses import dataclass
from typing import Any

@dataclass
class Node(object):
    pass

@dataclass
class Program(Node):
    instructions: Any

@dataclass
class Instructions(Node):
    instructions: Any

@dataclass
class EmptyInstruction(Node):
    pass

@dataclass
class If(Node):
    condition: Any
    instruction_if: Any
    instruction_else: Any = None

@dataclass
class For(Node):
    variable: Any
    range_: Any
    instruction: Any

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
class Variable(Node):
    name: Any

@dataclass
class Range(Node):
    start: Any
    end: Any

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
class MatrixElement(Node):
    variable: Any
    row: Any
    col: Any

@dataclass
class Assignment(Node):
    op: Any
    left: Any
    right: Any

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

@dataclass
class Matrix(Node):
    rows: Any

@dataclass
class Eye(Node):
    rows: Any
    cols: Any = None

@dataclass
class Zeros(Node):
    rows: Any
    cols: Any = None

@dataclass
class Ones(Node):
    rows: Any
    cols: Any = None

@dataclass
class Error(Node):
    pass
