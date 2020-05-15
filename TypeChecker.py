#!/usr/bin/python
import AST
from SymbolTable import *


class NodeVisitor(object):
    def visit(self, node, **kwargs):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method)
        return visitor(node)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.errorok = True
        self.table = SymbolTable()
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
        # self.visit(node.variable)
        self.visit(node.range_)
        self.loops += 1
        self.table.put(node.variable.name, Symbol('int'))
        self.visit(node.instruction)
        self.table.remove(node.variable.name)
        self.loops -= 1

    def visit_Range(self, node):
        start_type = self.visit(node.start).type
        if start_type not in ('int', 'unknown'):
            self.error('range start must be int', node.start.lineno)

        end_type = self.visit(node.end).type
        if end_type not in ('int', 'unknown'):
            self.error('range end must be int', node.end.lineno)

        return Symbol('range')

    def visit_While(self, node):
        self.visit(node.condition)
        self.loops += 1
        self.visit(node.instruction)
        self.loops -= 1

    def visit_Condition(self, node):
        left_type = self.visit(node.left).type
        right_type = self.visit(node.right).type
        types = {left_type, right_type}

        if 'unknown' in types:
            return

        if node.op in ('==', '!='):
            return

        if node.op in ('<', '>', '<=', '>='):
            if types.issubset({'int', 'float'}):
                return

        self.error(f'cannot perform: {left_type} {node.op} {right_type}', node.left.lineno)

    def visit_Break(self, node):
        if not self.loops:
            self.error('cannot use break outside loop', node.lineno)

    def visit_Continue(self, node):
        if not self.loops:
            self.error('cannot use continue outside loop', node.lineno)

    def visit_Return(self, node):
        if node.value is not None:
            value_type = self.visit(node.value).type
            if value_type not in ('int', 'unknown'):  # exit code
                self.error(f'cannot return {value_type}, must return int or nothing', node.value.lineno)

    def visit_Print(self, node):
        for arg in node.args:
            arg_type = self.visit(arg).type
            if arg_type == 'range':
                self.error(f'cannot print {arg_type}', arg.lineno)

    def visit_Assignment(self, node):
        if node.op == '=':
            if isinstance(node.left, AST.Variable):
                variable = node.left
                right_symbol = self.visit(node.right)
                try:
                    self.table.put(variable.name, right_symbol)
                except KeyError:
                    self.error(f'variable {variable.name} already has assigned value', variable.lineno)

            elif isinstance(node.left, AST.Reference):
                self.visit(node.left, as_rvalue=False)
                self.visit(node.right)
                # TODO: check if assignable

        # TODO: handle also +=, -=, *=, /=

    def visit_Variable(self, node):
        # as rvalue only
        variable_name = node.name
        try:
            return self.table.get(variable_name)
        except KeyError:
            self.error(f'variable {variable_name} not defined', node.lineno)
            return Symbol('unknown')

    def visit_Reference(self, node, as_rvalue=True):
        variable_type = self.visit(node.variable).type

        if variable_type in ('int', 'float', 'string'):
            self.error(f'{variable_type} is not subscriptable', node.variable.lineno)

        for index in node.indices:
            index_type = self.visit(index).type
            if index_type not in ('int', 'range', 'unknown'):
                self.error(f'index must be int or range', index.lineno)

        return Symbol('unknown')  # TODO: detect row, column or cell

    def visit_BinExpr(self, node):
        left_symbol = self.visit(node.left)
        right_symbol = self.visit(node.right)

        left_type = left_symbol.type
        right_type = right_symbol.type
        types = {left_type, right_type}

        if 'unknown' in types:
            return Symbol('unknown')

        if node.op == '+' and types == {'string'}:
            return Symbol('string')

        if node.op == '*' and left_type == 'string' and right_type == 'int':
            return Symbol('string')

        if node.op in ('+', '-', '*', '/'):
            if types == {'int'}:
                return Symbol('int')  # TODO: perform operations on constant operands?

            if types == {'int', 'float'}:
                return Symbol('float')

        if node.op in ('.+', '.-', '.*', './'):
            if types == {'vector'}:
                try:
                    left_length = left_symbol.params['length']
                    right_length = right_symbol.params['length']
                    if left_length != right_length:
                        self.error(f'vectors have different length ({left_length} vs. {right_length})', node.left.lineno)
                    return Symbol('vector', params={'length': left_length})
                except KeyError:
                    return Symbol('vector')

            if types == {'matrix'}:
                left_rows = left_symbol.params.get('rows', None)
                right_rows = right_symbol.params.get('rows', None)
                left_cols = left_symbol.params.get('cols', None)
                right_cols = right_symbol.params.get('cols', None)

                params = {}

                if left_rows is not None and right_rows is not None and left_rows != right_rows:
                    self.error(f'matrices have different number of rows ({left_rows} vs. {right_rows})', node.left.lineno)
                else:
                    params['rows'] = left_rows

                if left_cols is not None and right_cols is not None and left_cols != right_cols:
                    self.error(f'matrices have different number of columns ({left_cols} vs. {right_cols})', node.left.lineno)
                else:
                    params['cols'] = left_cols

                return Symbol('matrix', params=params)

        self.error(f'cannot perform {left_type} {node.op} {right_type}', node.left.lineno)
        return Symbol('unknown')

    def visit_UnaryExpr(self, node):
        expr_symbol = self.visit(node.expr)
        expr_type = expr_symbol.type

        if expr_type == 'unknown':
            return Symbol('unknown')

        if node.op == '-':
            if expr_type in ('int', 'float', 'vector', 'matrix'):
                return Symbol(expr_type, params=expr_symbol.params)

            self.error(f'cannot perform: {node.op}{expr_type}', node.expr.lineno)

        if node.op == "'":
            if expr_type == 'matrix':
                params = {}
                if 'cols' in expr_symbol.params:
                    params['rows'] = expr_symbol.params['cols']
                if 'rows' in expr_symbol.params:
                    params['cols'] = expr_symbol.params['rows']
                return Symbol(expr_type, params=params)

            self.error(f'cannot perform {expr_type}{node.op}', node.expr.lineno)

        return Symbol('unknown')

    def visit_IntNum(self, node):
        return Symbol('int', value=node.value)

    def visit_FloatNum(self, node):
        return Symbol('float', value=node.value)

    def visit_String(self, node):
        return Symbol('string', value=node.value)

    def visit_Vector(self, node):
        elements_types = set()

        for element in node.elements:
            element_type = self.visit(element).type
            if element_type not in ('unknown', 'int', 'float', 'vector'):
                self.error(f'vector element must be int or float', element.lineno)
            elements_types.add(element_type)

        if 'matrix' in elements_types:
            self.error('only 2D matrix supported', element.lineno)
            return Symbol('matrix', params={'rows': len(node.elements)})

        if 'vector' in elements_types:
            if elements_types == {'vector'}:
                lengths = {len(element.elements) for element in node.elements}
                if len(lengths) > 1:
                    self.error(f'matrix rows must be the same length', node.elements[0].lineno)
            else:
                self.error(f'matrix rows must be vectors', node.elements[0].lineno)

            return Symbol('matrix', params={'rows': len(node.elements), 'cols': len(node.elements[0].elements)})

        return Symbol('vector', params={'length': len(node.elements)})

    def visit_MatrixSpecialFunction(self, node):
        # TODO: check non-negativity

        rows_symbol = self.visit(node.rows)
        if rows_symbol.type not in ('unknown', 'int'):
            self.error(f'number of rows must be int', node.rows.lineno)

        if node.cols is not None:
            cols_symbol = self.visit(node.cols)
            if cols_symbol.type not in ('unknown', 'int'):
                self.error(f'number of columns must be int', node.cols.lineno)

        rows_value = rows_symbol.value
        cols_value = cols_symbol.value if node.cols is not None else rows_value

        return Symbol('matrix', params={'rows': rows_value, 'cols': cols_value})

    visit_Eye = visit_MatrixSpecialFunction
    visit_Zeros = visit_MatrixSpecialFunction
    visit_Ones = visit_MatrixSpecialFunction

    def visit_Error(self, node):
        return Symbol('unknown')
