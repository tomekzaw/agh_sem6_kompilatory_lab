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
        '*': np.dot if isinstance(left, np.ndarray) and isinstance(right, np.ndarray) else operator.mul,  # works for `string * int` as well
        '/': operator.truediv,
        '+=': operator.iadd,  # for compound assignments (in-place), works for `string += string` as well
        '-=': operator.isub,
        '*=': operator.imul,  # works for `string *= int` as well
        '/=': operator.itruediv,
        '.+': np.add,  # for matrix element-wise operations
        '.-': np.subtract,
        '.*': np.multiply,
        './': np.divide,
    }[op](left, right)


class Interpreter:
    def __init__(self, catch_runtime_errors=True):
        self.memory_stack = MemoryStack()
        self.catch_runtime_errors = catch_runtime_errors

    def error(self, message: str, lineno: int):
        raise RuntimeError(f'{message} (line {lineno})')

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
            if self.catch_runtime_errors:
                print(f'*** Runtime error: {err} ***')
            else:
                raise err  # for testing purposes

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
        return slice(start, end)  # works nice for references, but has to be converted into range when used as for-loop iterator

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
        right = node.right.accept(self)

        if isinstance(node.left, Variable):
            name = node.left.name
            if node.op == '=':  # simple assignment
                if isinstance(right, np.ndarray):
                    right = right.copy()
                value = right
            else:  # compound assigment (+=, -=, *=, /=)
                left = self.memory_stack.get(name)
                value = eval_binexpr(node.op[0], left, right)
            self.memory_stack.set(name, value)

        else:  # Reference
            variable_name = node.left.variable.name
            variable_value = self.memory_stack.get(variable_name)
            if len(variable_value.shape) != len(node.left.indices):
                self.error(f'invalid number of indices for {variable_name}', node.lineno)
            indices = tuple(index.accept(self) for index in node.left.indices)
            try:
                if node.op == '=':  # simple assignment
                    variable_value[indices] = right
                else:  # compound assigment (+=, -=, *=, /=)
                    eval_binexpr(node.op, variable_value[indices], right)
            except ValueError:
                # TODO: manually check shapes before
                self.error('invalid assignment to reference', node.lineno)

    @when(Variable)
    def visit(self, node):  # as rvalue only
        return self.memory_stack.get(node.name)

    @when(Reference)
    def visit(self, node):  # as rvalue only
        variable_name = node.variable.name
        variable_value = self.memory_stack.get(variable_name)
        shape = variable_value.shape
        if len(shape) != len(node.indices):
            self.error(f'invalid number of indices for {variable_name}', node.lineno)
        indices = tuple(index.accept(self) for index in node.indices)
        for i, (index, size) in enumerate(zip(indices, shape)):
            if isinstance(index, slice):
                index = index.stop
            if index < 0:
                self.error('negative index for axis {i}', node.indices[i].lineno)
            if index > size:
                self.error(f'index {index} out of bounds for axis {i} with size {size}', node.indices[i].lineno)
        return variable_value[indices]

    @when(BinExpr)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        if node.op == '/' and right == 0:
            self.error('division by zero', node.lineno)
        if node.op == '*':
            if isinstance(left, str) and right < 0:
                self.error('cannot repeat negative number of times', node.lineno)
            if isinstance(left, np.ndarray) and isinstance(right, np.ndarray):
                if left.shape[1] != right.shape[0]:
                    self.error('cannot mutliply matrices with unmatching shapes', node.lineno)
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
        rows, cols = self._interpret_params(node, np.eye)
        return np.eye(rows, cols)

    @when(Zeros)
    def visit(self, node):
        rows, cols = self._interpret_params(node, np.eye)
        return np.zeros((rows, cols))

    @when(Ones)
    def visit(self, node):
        rows, cols = self._interpret_params(node, np.eye)
        return np.ones((rows, cols))

    def _interpret_params(self, node, func):
        rows = node.rows.accept(self)
        if rows < 0:
            self.error('negative number of rows is not allowed', node.rows.lineno)
        cols = node.cols.accept(self) if node.cols is not None else rows
        if cols < 0:
            self.error('negative number of columns is not allowed', node.cols.lineno)
        return rows, cols

    @when(Error)
    def visit(self, node):
        raise self.error(str(node), node.lineno)
