import sys
import operator
import numpy as np
from AST import *
from visit import *
from Memory import *
from Exceptions import *

sys.setrecursionlimit(10000)


def eval_binexpr(op, left, right):
    """
    Calculates value of binary expression.
    This function is utilized both in BinExpr node (+, -, *, /, .+, .-, .*, ./)
    and Assignment node for compound assignments (+=, -=, *=, /=).
    """
    return {
        '+': operator.add,  # works for `string + string` as well
        '-': operator.sub,
        '*': operator.mul,  # works for `string * int` as well
        '/': operator.truediv,
        '.+': np.add,
        '.-': np.subtract,
        '.*': np.multiply,
        './': np.divide,
    }[op](left, right)


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
            if not isinstance(exit_code, int):  # invalid exit code (must be int)
                exit_code = -1
            sys.exit(exit_code)
        except RuntimeError as err:
            print(f'*** Runtime error: {err} ***')

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
        try:
            for i in range(start, end + 1):
                try:
                    self.memory_stack.push(Memory('for', {variable_name: i}))
                    # self.memory_stack.insert(variable_name, i)
                    node.instruction.accept(self)
                except ContinueException:
                    pass
                finally:
                    self.memory_stack.pop()
        except BreakException:
            pass

    @when(Range)
    def visit(self, node):
        start = node.start.accept(self)
        end = node.end.accept(self)
        return slice(start, end)  # for references, for for-loop will be converted to range

    @when(While)
    def visit(self, node):
        try:
            while node.condition.accept(self):
                try:
                    self.memory_stack.push(Memory('while'))
                    node.instruction.accept(self)
                except ContinueException:
                    pass
                finally:
                    self.memory_stack.pop()
        except BreakException:
            pass

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

        name = node.left.name

        if node.op == '=':
            value = node.right.accept(self)
        else:  # compound assigment (+=, -=, *=, /=)
            left = self.memory_stack.get(name)
            right = node.right.accept(self)
            op = node.op[0]
            value = eval_binexpr(op, left, right)

        self.memory_stack.set(name, value)

    @when(Variable)
    def visit(self, node):  # as rvalue only
        return self.memory_stack.get(node.name)

    @when(Reference)
    def visit(self, node):  # as rvalue only
        variable_value = self.memory_stack.get(node.variable.name)
        indices = tuple(index.accept(self) for index in node.indices)
        return variable_value[indices]

    @when(BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if node.op == '/' and right == 0:
            raise RuntimeError('Division by zero')
        # matrix element-wise division returns NaNs or infs
        return eval_binexpr(node.op, left, right)

    @when(UnaryExpr)
    def visit(self, node):
        expr = node.expr.accept(self)
        return {
            '-': operator.neg,
            "'": np.transpose,
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
        rows = node.rows.accept(self)
        cols = node.cols.accept(self) if node.cols is not None else rows
        return np.eye(rows, cols)

    @when(Zeros)
    def visit(self, node):
        rows = node.rows.accept(self)
        cols = node.cols.accept(self) if node.cols is not None else rows
        return np.zeros((rows, cols))

    @when(Ones)
    def visit(self, node):
        rows = node.rows.accept(self)
        cols = node.cols.accept(self) if node.cols is not None else rows
        return np.ones((rows, cols))

    @when(Error)
    def visit(self, node):
        raise RuntimeError(str(node))
