#!/usr/bin/python
import AST


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.errorok = True

    def error(self, message, kind='type'):
        self.errorok = False
        print(f'{kind} error: {message}')

    def visit_If(self, node):
        self.visit(node.condition)
        self.visit(node.instruction_then)
        if node.instruction_else is not None:
            self.visit(node.instruction_else)

    def visit_Range(self, node):
        start_type = self.visit(node.start)
        if start_type not in ('int', 'unknown'):
            self.error('range start must be int')

        end_type = self.visit(node.start)
        if end_type not in ('int', 'unknown'):
            self.error('range end must be int')

        return 'range'

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

        self.error(f'cannot perform: {left_type} {node.op} {right_type}')

    def visit_Break(self, node):
        # TODO: check if inside loop
        pass

    def visit_Continue(self, node):
        # TODO: check if inside loop
        pass

    def visit_Return(self, node):
        if node.value is not None:
            value_type = self.visit(node.value)
            if value_type not in ('int', 'unknown'):  # exit code
                self.error(f'cannot return {value_type}, must return int or nothing')

    def visit_Print(self, node):
        for arg in args:
            arg_type = self.visit(arg)
            if arg_type not in ('unknown', 'int', 'float', 'string', 'vector', 'matrix'):
                self.error(f'cannot print {arg_type}')

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
            self.error(f'{variable_type} is not subscriptable')

        for index in node.indices:
            index_type = self.visit(index)
            if index_type not in ('unknown', 'int', 'range'):
                self.error(f'index must be int or range')

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
            if types == {'matrix'}:
                return 'matrix'

        self.error(f'cannot perform {left_type} {node.op} {right_type}')
        return 'unknown'

    def visit_UnaryExpr(self, node):
        expr_type = self.visit(node.expr)

        if expr_type == 'unknown':
            return 'unknown'

        if node.op == '-':
            if expr_type in ('int', 'float'):
                return expr_type

            self.error(f'cannot perform: {node.op}{expr_type}')
            return 'unknown'

        if node.op == "'":
            if expr_type == 'matrix':
                return expr_type

            self.error(f'cannot perform {expr_type}{node.op}')
            return 'unknown'

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
                self.error(f'vector element must be int or float')
            elements_types.add(element_type)

        if 'vector' in elements_types:
            if elements_types == {'vector'}:
                lengths = {len(element.elements) for element in node.elements}
                if len(lengths) > 1:
                    self.error(f'matrix rows must be the same length')
            else:
                self.error(f'matrix rows must be vectors')

        return f'vector'

    def visit_MatrixSpecialFunction(self, node):
        rows_type = self.visit(node.rows)
        if rows_type not in ('unknown', 'int'):
            self.error(f'number of rows must be int')

        if node.cols is not None:
            cols_type = self.visit(node.cols)
            if cols_type not in ('unknown', 'int'):
                self.error(f'number of columns must be int')

        return 'matrix'

    visit_Eye = visit_MatrixSpecialFunction
    visit_Zeros = visit_MatrixSpecialFunction
    visit_Ones = visit_MatrixSpecialFunction

    def visit_Error(self, node):
        return 'unknown'
