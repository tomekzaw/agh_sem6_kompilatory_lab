import sys
import operator
import numpy as np
from AST import *
from visit import *
from Memory import *
from Exceptions import *

sys.setrecursionlimit(10000)


class Interpreter:
    def __init__(self):
        self.memory_stack = MemoryStack()

    @on('node')
    def visit(self, node):
        pass

    @when(Node)
    def visit(self, node):
        raise Exception(f'visit method not defined for {node.__class__.__name__}')

    @when(Program)
    def visit(self, node):
        try:
            node.instructions.accept(self)
        except ReturnValueException as exc:
            exit_code = exc.value
            if not isinstance(exit_code, int):
                exit_code = -1
            sys.exit(exit_code)
        except RuntimeError as err:
            print(f'Runtime error: {err}')

    @when(Instructions)
    def visit(self, node):
        for instruction in node.instructions:
            instruction.accept(self)

    @when(If)
    def visit(self, node):
        if node.condition.accept(self):
            node.instruction_then.accept(self)
        elif node.instruction_else is not None:
            node.instruction_else.accept(self)

    @when(For)
    def visit(self, node):
        variable_name = node.variable.name
        range_ = node.range_.accept(self)
        start, end = range_.start, range_.stop

        self.memory_stack.push(Memory('for'))
        self.memory_stack.insert(variable_name, None)
        for i in range(start, end+1):
            self.memory_stack.set(variable_name, i)
            node.instruction.accept(self)
        self.memory_stack.pop()

    @when(Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return slice(start, end)  # for references, for for-loop will be converted to range

    @when(While)
    def visit(self, node):
        while node.condition.accept(self):
            node.instruction.accept(self)

    @when(Condition)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return {
            '==': operator.eq,
            '!=': operator.ne,
            '<': operator.lt,
            '>': operator.gt,
            '<=': operator.le,
            '>=': operator.ge,
        }[node.op](left, right)

    @when(Break)
    def visit(self, node):
        raise BreakException()

    @when(Continue)
    def visit(self, node):
        raise ContinueException()

    @when(Return)
    def visit(self, node):
        value = node.value.accept(self) if node.value is not None else None
        raise ReturnValueException(value)

    @when(Print)
    def visit(self, node):
        print(', '.join(str(arg.accept(self)) for arg in node.args))

    @when(Assignment)
    def visit(self, node):
        if not isinstance(node.left, Variable):
            raise NotImplementedError('Reference assignments not implemented yet')  # TODO implement reference assignments

        if node.op in ('+=', '-=', '*=', '/='):
            raise NotImplementedError('Compound assignments not implemented yet')  # TODO implement compound assignments

        name = node.left.name
        value = node.right.accept(self)
        self.memory_stack.insert(name, value)

    @when(Variable)
    def visit(self, node):
        # as rvalue only
        return self.memory_stack.get(node.name)

    @when(Reference)
    def visit(self, node):
        # as rvalue only
        raise NotImplementedError('References not implemented yet')  # TODO implement references

    @when(BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if node.op == '/' and right == 0:
            raise RuntimeError('Division by zero')
        return {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
        }[node.op](left, right)


    @when(UnaryExpr)
    def visit(self, node):
        expr = node.expr.accept(self)
        return {
            '-': operator.neg,
            "'": lambda x: x.T,
        }[node.op](expr)

    @when(IntNum)
    def visit(self, node):
        return node.value

    @when(FloatNum)
    def visit(self, node):
        return node.value

    @when(String)
    def visit(self, node):
        return node.value

    @when(Vector)
    def visit(self, node):
        elements = tuple(element.accept(self) for element in node.elements)
        return np.array(elements)

    @when(Eye)
    def visit(self, node):
        rows = node.rows
        cols = node.cols if node.cols is not None else rows
        return np.eye(rows, cols)

    @when(Zeros)
    def visit(self, node):
        rows = node.rows
        cols = node.cols if node.cols is not None else rows
        return np.zeros((rows, cols))

    @when(Ones)
    def visit(self, node):
        rows = node.rows
        cols = node.cols if node.cols is not None else rows
        return np.ones((rows, cols))

    @when(Error)
    def visit(self, node):
        raise RuntimeError(str(node))
