from AST import *
from visit import *
import sys

sys.setrecursionlimit(10000)


class Interpreter(object):
    @on('node')
    def visit(self, node):
        pass

    # @when(AST.IntNum)
    # def visit(self, node):
    #     return node.value

    # @when(AST.BinExpr)
    # def visit(self, node):
    #     left = node.left.accept(self)
    #     right = node.right.accept(self)
    #     if node.op == '/' and right == 0:
    #         raise RuntimeError('Division by zero')
    #     return {
    #         '+': operator.add,
    #         '-': operator.sub,
    #         '*': operator.mul,
    #         '/': operator.div,
    #     }[node.op](left, right)

    # @when(AST.Assignment)
    # def visit(self, node):
    #     value = node.right.accept(self)
    #     print(f'assignment: {value}')

    @when(Program)
    def visit(self, node):
        print('visiting Program')
        # node.instructions.accept(self)
