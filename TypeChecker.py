#!/usr/bin/python
import AST


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.errorok = True
        self.loops = 0

    def error(self, message: str, lineno: int):
        self.errorok = False
        print(f'line {lineno}: {message}')

    def visit_Program(self, node):
        self.visit(node.instructions)

    def visit_Instructions(self, node):
        for instruction in node.instructions:
            self.visit(instruction)

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.instruction_then)
        if node.instruction_else is not None:
            self.visit(node.instruction_else)

    def visit_For(self, node):
        self.visit(node.variable)
        # TODO: variable scope
        self.visit(node.range_)
        self.loops += 1
        self.visit(node.instruction)
        self.loops -= 1

    def visit_Range(self, node):
        start_type = self.visit(node.start)
        if start_type not in ('int', 'unknown'):
            self.error('range start must be int', node.start.lineno)

        end_type = self.visit(node.start)
        if end_type not in ('int', 'unknown'):
            self.error('range end must be int', node.end.lineno)

        return 'range'

    def visit_While(self, node):
        self.visit(node.condition)
        self.loops += 1
        self.visit(node.instruction)
        self.loops -= 1

    def visit_Condition(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        types = {left_type, right_type}

        if 'unknown' in types:
            return 'unknown'

        if node.op in ('==', '!='):
            return

        if node.op in ('<', '>', '<=', '>='):
            if types.issubset({'int', 'float'}):
                return

        self.error(f'cannot perform: {left_type} {node.op} {right_type}', node.left.lineno)

    def visit_Break(self, node):
        if self.loops == 0:
            self.error('cannot use break outside loop', node.lineno)

    def visit_Continue(self, node):
        if self.loops == 0:
            self.error('cannot use continue outside loop', node.lineno)

    def visit_Return(self, node):
        if node.value is not None:
            value_type = self.visit(node.value)
            if value_type not in ('int', 'unknown'):  # exit code
                self.error(f'cannot return {value_type}, must return int or nothing', node.value.lineno)

    def visit_Print(self, node):
        for arg in args:
            arg_type = self.visit(arg)
            if arg_type not in ('unknown', 'int', 'float', 'string', 'vector', 'matrix'):
                self.error(f'cannot print {arg_type}', arg.lineno)

    def visit_Assignment(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)

        if right_type == 'unknown':
            return

    def visit_Variable(self, node):
        # TODO: check if exists in symbol table
        return 'unknown'

    def visit_Reference(self, node):
        variable_type = self.visit(node.variable)

        if variable_type in ('int', 'float', 'string'):
            self.error(f'{variable_type} is not subscriptable', node.variable.lineno)

        for index in node.indices:
            index_type = self.visit(index)
            if index_type not in ('unknown', 'int', 'range'):
                self.error(f'index must be int or range', index.lineno)

        return 'unknown'

    def visit_BinExpr(self, node):
        left_type = self.visit(node.left)
        right_type = self.visit(node.right)
        types = {left_type, right_type}

        if 'unknown' in types:
            return 'unknown'

        if node.op == '+' and types == {'string'}:
            return 'string'

        if node.op == '*' and left_type == 'string' and right_type == 'int':
            return 'string'

        if node.op in ('+', '-', '*', '/'):
            if types == {'int'}:
                return 'int'

            if types == {'int', 'float'}:
                return 'float'

        if node.op in ('.+', '.-', '.*', './'):
            if types == {'vector'}:
                if isinstance(node.left, AST.Vector) and isinstance(node.right, AST.Vector):
                    left_shape = len(node.left.elements)
                    right_shape = len(node.right.elements)
                    if left_shape != right_shape:
                        self.error(f'different shapes {left_shape} vs {right_shape}', node.left.lineno)
                return 'vector'

            if types == {'matrix'}:
                if isinstance(node.left, AST.Vector) and isinstance(node.right, AST.Vector):
                    left_shape = (len(node.left.elements), len(node.left.elements[0].elements))
                    right_shape = (len(node.right.elements), len(node.right.elements[0].elements))
                    if left_shape != right_shape:
                        self.error(f'different shapes {left_shape} vs {right_shape}', node.left.lineno)
                return 'matrix'

        self.error(f'cannot perform {left_type} {node.op} {right_type}', node.left.lineno)
        return 'unknown'

    def visit_UnaryExpr(self, node):
        expr_type = self.visit(node.expr)

        if expr_type == 'unknown':
            return 'unknown'

        if node.op == '-':
            if expr_type in ('int', 'float', 'vector', 'matrix'):
                return expr_type

            self.error(f'cannot perform: {node.op}{expr_type}', node.expr.lineno)

        if node.op == "'":
            if expr_type == 'matrix':
                return expr_type

            self.error(f'cannot perform {expr_type}{node.op}', node.expr.lineno)

        return 'unknown'

    def visit_IntNum(self, node):
        return 'int'

    def visit_FloatNum(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Vector(self, node):
        elements_types = set()

        for element in node.elements:
            element_type = self.visit(element)
            if element_type not in ('unknown', 'int', 'float', 'vector'):
                self.error(f'vector element must be int or float', element.lineno)
            elements_types.add(element_type)

        if 'matrix' in elements_types:
            self.error('only 2D matrix supported', element.lineno)
            return 'matrix'

        if 'vector' in elements_types:
            if elements_types == {'vector'}:
                lengths = {len(element.elements) for element in node.elements}
                if len(lengths) > 1:
                    self.error(f'matrix rows must be the same length', node.elements[0].lineno)
            else:
                self.error(f'matrix rows must be vectors', node.elements[0].lineno)

            return 'matrix'

        return 'vector'

    def visit_MatrixSpecialFunction(self, node):
        # TODO: check non-negativity

        rows_type = self.visit(node.rows)
        if rows_type not in ('unknown', 'int'):
            self.error(f'number of rows must be int', node.rows.lineno)

        if node.cols is not None:
            cols_type = self.visit(node.cols)
            if cols_type not in ('unknown', 'int'):
                self.error(f'number of columns must be int', node.cols.lineno)

        return 'matrix'
        # TODO: return shape if available

    visit_Eye = visit_MatrixSpecialFunction
    visit_Zeros = visit_MatrixSpecialFunction
    visit_Ones = visit_MatrixSpecialFunction

    def visit_Error(self, node):
        return 'unknown'
