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
        if node.instruction_else is None:
            self.visit(node.instruction_then)
        else:
            self.table.pushScope('then')
            self.visit(node.instruction_then)
            then_scope = self.table.popScope()

            self.table.pushScope('else')
            self.visit(node.instruction_else)
            else_scope = self.table.popScope()

            for name in set(then_scope.symbols.keys()) & set(else_scope.symbols.keys()):
                symbol1 = then_scope.symbols[name]
                symbol2 = else_scope.symbols[name]
                type1 = symbol1.type
                type2 = symbol2.type
                if {type1, type2} != 'unknown':
                    if type1 != type2:
                        self.error(f'variable {name} can be either {type1} or {type2}', node.instruction_then.lineno)
                        else_scope.symbols[name] = Symbol('unknown')
                    elif type1 == 'vector':
                        if 'length' in symbol1.params.keys() & symbol2.params.keys():
                            length1 = symbol1.params['length']
                            length2 = symbol2.params['length']
                            self.error(f'{name} vector can have length of either {length1} or {length2}', node.instruction_then.lineno)
                            del else_scope.symbols[name].params['length']
                    elif type1 == 'matrix':
                        if 'rows' in symbol1.params.keys() & symbol2.params.keys():
                            rows1 = symbol1.params['rows']
                            rows2 = symbol2.params['rows']
                            self.error(f'{name} matrix can have either {rows1} or {rows2} rows', node.instruction_then.lineno)
                            del else_scope.symbols[name].params['rows']
                        if 'cols' in symbol1.params.keys() & symbol2.params.keys():
                            cols1 = symbol1.params['cols']
                            cols2 = symbol2.params['cols']
                            self.error(f'{name} matrix can have either {cols1} or {cols2} cols', node.instruction_then.lineno)
                            del else_scope.symbols[name].params['cols']
                # TODO: vector, matrix

            self.table.current_scope.symbols.update({**then_scope.symbols, **else_scope.symbols})

    def visit_For(self, node):
        # self.visit(node.variable)
        self.visit(node.range_)
        self.loops += 1
        self.table.pushScope('for')
        loop_variable_name = node.variable.name
        if self.table.has(loop_variable_name):
            self.error(f'cannot override variable {loop_variable_name}', node.variable.lineno)
        self.table.put(loop_variable_name, Symbol('int', params={'loop_variable': True}))
        self.visit(node.instruction)
        # self.table.remove(node.variable.name)
        self.table.popScope()
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
        self.table.pushScope('while')
        self.loops += 1
        self.visit(node.instruction)
        self.loops -= 1
        self.table.popScope()

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
            self.error('break statement not within loop', node.lineno)

    def visit_Continue(self, node):
        if not self.loops:
            self.error('continue statement not within loop', node.lineno)

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
                if self.table.has(variable.name):
                    self.error(f'cannot overwrite variable {variable.name}', variable.lineno)
                self.table.put(variable.name, right_symbol)

            elif isinstance(node.left, AST.Reference):
                self.visit(node.left, as_rvalue=False)
                self.visit(node.right)
                # TODO: check if assignable

        if node.op in ('+=', '-=', '*=', '/='):
            if isinstance(node.left, AST.Variable):
                variable_node = node.left
                try:
                    variable_symbol = self.table.get(variable_node.name)
                    modifier_symbol = self.visit(node.right)

                    if 'loop_variable' in variable_symbol.params and variable_symbol.params['loop_variable']:
                        self.error(f'cannot modify value of loop variable {variable_node.name}', variable_node.lineno)
                    elif 'unknown' not in {variable_symbol.type, modifier_symbol.type} and variable_symbol.type != modifier_symbol.type:
                        # TODO: include vectors length, matrix shape etc. (maybe create classes for types and add compatibility function)
                        self.error(f'cannot modify variable {variable_node.name} of type {variable_symbol.type} with {modifier_symbol.type}', variable_node.lineno)
                except KeyError:
                    self.error(f'variable {variable_name} not defined', variable_node.lineno)

    def visit_Variable(self, node):
        # as rvalue or reference only
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
                self.error('index must be int or range', index.lineno)

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
                self.error(f'vector element must be int or float, not {element_type}', element.lineno)
            elements_types.add(element_type)

        if 'matrix' in elements_types:
            self.error('only 2D matrix supported', element.lineno)
            return Symbol('matrix', params={'rows': len(node.elements)})

        if 'vector' in elements_types:
            if elements_types == {'vector'}:
                lengths = {len(element.elements) for element in node.elements}
                if len(lengths) > 1:
                    self.error('matrix rows must be the same length', node.elements[0].lineno)
            else:
                self.error('matrix rows must be vectors', node.elements[0].lineno)

            return Symbol('matrix', params={'rows': len(node.elements), 'cols': len(node.elements[0].elements)})

        return Symbol('vector', params={'length': len(node.elements)})

    def visit_MatrixSpecialFunction(self, node):
        rows_symbol = self.visit(node.rows)
        if rows_symbol.type not in ('unknown', 'int'):
            self.error('number of rows must be int', node.rows.lineno)
        elif rows_symbol.value is not None and rows_symbol.value < 0:
            self.error('number of rows must non-negative', node.rows.lineno)

        if node.cols is not None:
            cols_symbol = self.visit(node.cols)
            if cols_symbol.type not in ('unknown', 'int'):
                self.error('number of columns must be int', node.cols.lineno)
            elif cols_symbol.value is not None and cols_symbol.value < 0:
                self.error('number of columns must non-negative', node.cols.lineno)

        rows_value = rows_symbol.value
        cols_value = cols_symbol.value if node.cols is not None else rows_value

        return Symbol('matrix', params={'rows': rows_value, 'cols': cols_value})

    visit_Eye = visit_MatrixSpecialFunction
    visit_Zeros = visit_MatrixSpecialFunction
    visit_Ones = visit_MatrixSpecialFunction

    def visit_Error(self, node):
        return Symbol('unknown')
