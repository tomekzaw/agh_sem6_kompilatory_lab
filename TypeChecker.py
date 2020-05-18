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

            for name in then_scope.symbols.keys() & else_scope.symbols.keys():
                type1 = then_scope.symbols[name].type
                type2 = else_scope.symbols[name].type
                if type1 != type2:
                    self.error(f'variable {name} can be either {type1} or {type2}', node.instruction_then.lineno)
                    else_scope.symbols[name] = Symbol(type=Unknown())

            self.table.current_scope.symbols.update({**then_scope.symbols, **else_scope.symbols})

    def visit_For(self, node):
        # self.visit(node.variable)  # will be handled later on
        self.visit(node.range_)
        self.loops += 1
        self.table.pushScope('for')

        loop_variable_name = node.variable.name
        if self.table.has(loop_variable_name):
            self.error(f'loop variable cannot override existing variable', node.variable.lineno)
        self.table.put(loop_variable_name, Symbol(Int(), readonly=True))
        self.visit(node.instruction)
        # self.table.remove(node.variable.name)  # will be automatically deleted

        self.table.popScope()
        self.loops -= 1

    def visit_Range(self, node):
        start_type = self.visit(node.start).type
        if start_type != Int():
            self.error('range start must be int', node.start.lineno)

        end_type = self.visit(node.end).type
        if end_type != Int():
            self.error('range end must be int', node.end.lineno)

        return Symbol(type=Range())

    def visit_While(self, node):
        self.visit(node.condition)
        self.table.pushScope('while')
        self.loops += 1
        self.visit(node.instruction)
        self.loops -= 1
        self.table.popScope()

    def visit_Condition(self, node):
        type1 = self.visit(node.left).type
        type2 = self.visit(node.right).type

        if isinstance(type1, Unknown) or isinstance(type2, Unknown):
            return

        if node.op in ('==', '!='):
            return

        if node.op in ('<', '>', '<=', '>='):
            if isinstance(type1, (Int, Float)) and isinstance(type2, (Int, Float)):
                return

        self.error(f'cannot perform: {type1} {node.op} {type2}', node.left.lineno)

    def visit_Break(self, node):
        if not self.loops:
            self.error('break statement not within loop', node.lineno)

    def visit_Continue(self, node):
        if not self.loops:
            self.error('continue statement not within loop', node.lineno)

    def visit_Return(self, node):
        if node.value is not None:
            value_type = self.visit(node.value).type
            if value_type != Int():  # exit code
                self.error(f'cannot return {value_type}, must return int or nothing', node.value.lineno)

    def visit_Print(self, node):
        for arg in node.args:
            arg_type = self.visit(arg).type
            if arg_type == Range():
                self.error(f'cannot print {arg_type}', arg.lineno)

    def visit_Assignment(self, node):
        if node.op == '=':
            if isinstance(node.left, AST.Variable):
                variable = node.left
                right_symbol = self.visit(node.right)
                if self.table.has(variable.name):  # handles loop variables too
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

                    if variable_symbol.readonly:
                        self.error(f'cannot modify value of loop variable {variable_node.name}', variable_node.lineno)

                    if variable_symbol.type != modifier_symbol.type:
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
            return Symbol(type=Unknown())

    def visit_Reference(self, node, as_rvalue=True):
        variable_type = self.visit(node.variable).type

        if isinstance(variable_type, (Int, Float, String)):
            self.error(f'{variable_type} is not subscriptable', node.variable.lineno)

        for index in node.indices:
            index_type = self.visit(index).type
            if not isinstance(index_type, (Unknown, Int, Range)):
                self.error('index must be int or range', index.lineno)

        return Symbol(type=Unknown())  # TODO: detect row, column or cell

    def visit_BinExpr(self, node):
        left_symbol = self.visit(node.left)
        right_symbol = self.visit(node.right)

        left_type = left_symbol.type
        right_type = right_symbol.type

        if isinstance(left_type, Unknown) or isinstance(right_type, Unknown):
            return Symbol(type=Unknown())

        if node.op == '+' and isinstance(left_type, String) and isinstance(right_type, String):
            return Symbol(type=String())

        if node.op == '*' and isinstance(left_type, String) and isinstance(right_type, Int):
            return Symbol(type=String())

        if node.op in ('+', '-', '*', '/'):
            if isinstance(left_type, Int) and isinstance(right_type, Int):
                return Symbol(type=Int())  # TODO: perform operations on constant operands?

            if isinstance(left_type, (Int, Float)) and isinstance(right_type, (Int, Float)):
                return Symbol(type=Float())

        if node.op in ('.+', '.-', '.*', './'):
            if isinstance(left_type, Vector) and isinstance(right_type, Vector):
                if left_type != right_type:
                    self.error(f'vectors have different length ({left_type.length} vs. {right_type.length})', node.left.lineno)
                    return Symbol(type=Vector())
                else:
                    return Symbol(type=Vector(length=left_type.length))

            if isinstance(left_type, Matrix) and isinstance(right_type, Matrix):
                if left_type != right_type:
                    self.error(f'matrices have different shape', node.left.lineno)
                    return Symbol(type=Matrix())
                else:
                    return Symbol(type=Matrix(rows=left_type.rows, cols=left_type.cols))

                # TODO: manually check number of rows and columns, leave if they are the same

        self.error(f'cannot perform {left_type} {node.op} {right_type}', node.left.lineno)
        return Symbol(type=Unknown())

    def visit_UnaryExpr(self, node):
        expr_symbol = self.visit(node.expr)
        expr_type = expr_symbol.type

        if isinstance(expr_type, Unknown):
            return expr_symbol

        if node.op == '-':
            if isinstance(expr_type, (Int, Float, Vector, Matrix)):
                return expr_symbol
                # TODO: handle non-negativity property?

            self.error(f'cannot perform: {node.op}{expr_type}', node.expr.lineno)

        if node.op == "'":
            if isinstance(expr_type, Matrix):
                rows, cols = expr_type.cols, expr_type.rows
                return Symbol(type=Matrix(rows=rows, cols=cols))

            self.error(f'cannot perform {expr_type}{node.op}', node.expr.lineno)

        return Symbol(type=Unknown())

    def visit_IntNum(self, node):
        return Symbol(type=Int(), value=node.value)

    def visit_FloatNum(self, node):
        return Symbol(type=Float(), value=node.value)

    def visit_String(self, node):
        return Symbol(type=String(), value=node.value)

    def visit_Vector(self, node):
        elements_types = []

        for element in node.elements:
            element_type = self.visit(element).type
            if not isinstance(element_type, (Unknown, Int, Float, Vector)):
                self.error(f'vector element must be int or float, not {element_type}', element.lineno)
            elements_types.append(element_type.__class__)

        if Matrix in elements_types:
            self.error('only 2D matrix supported', element.lineno)
            return Symbol(type=Matrix(rows=len(node.elements)))

        if Vector in elements_types:
            if elements_types == [Vector] * len(elements_types):  # TODO: seriously, fix that
                lengths = {len(element.elements) for element in node.elements}
                if len(lengths) > 1:
                    self.error('matrix rows must be the same length', node.elements[0].lineno)
            else:
                self.error('matrix rows must be vectors', node.elements[0].lineno)

            return Symbol(type=Matrix(rows=len(node.elements), cols=len(node.elements[0].elements)))

        return Symbol(type=Vector(length=len(node.elements)))

    def visit_MatrixSpecialFunction(self, node):
        rows_symbol = self.visit(node.rows)
        if rows_symbol.type.__class__ not in (Unknown, Int):
            self.error('number of rows must be int', node.rows.lineno)
        elif rows_symbol.value is not None and rows_symbol.value < 0:
            self.error('number of rows must be non-negative', node.rows.lineno)

        if node.cols is not None:
            cols_symbol = self.visit(node.cols)
            if cols_symbol.type.__class__ not in (Unknown, Int):
                self.error('number of columns must be int', node.cols.lineno)
            elif cols_symbol.value is not None and cols_symbol.value < 0:
                self.error('number of columns must non-negative', node.cols.lineno)

        rows_value = rows_symbol.value
        cols_value = cols_symbol.value if node.cols is not None else rows_value

        return Symbol(type=Matrix(rows=rows_value, cols=cols_value))

    visit_Eye = visit_MatrixSpecialFunction
    visit_Zeros = visit_MatrixSpecialFunction
    visit_Ones = visit_MatrixSpecialFunction

    def visit_Error(self, node):
        return Symbol(type=Unknown())
