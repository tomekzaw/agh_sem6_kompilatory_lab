import sys
from itertools import count
from scanner import lexer, find_column  # noqa
from Mparser import parser
from TreePrinter import TreePrinter  # noqa
from TypeChecker import TypeChecker
from Interpreter import Interpreter


def read():
    # return sys.stdin.read()
    text = ""
    for ln in count(1):
        try:
            text += input(f'{ln:>4d} |  ') + '\n'
        except (RuntimeError, EOFError):
            break
    return text


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    else:
        text = read()

    # lexer.input(text)
    # for token in lexer:
    #     # column = find_column(text, token)
    #     # print('(%d,%d): %s(%s)' % (token.lineno, column, token.type, token.value))
    #     print('(%d): %s(%s)' % (token.lineno, token.type, token.value))

    ast = parser.parse(text, lexer=lexer)
    if not parser.errorok:
        raise SystemExit

    # ast.printTree()

    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    if not typeChecker.errorok:
        raise SystemExit

    ast.accept(Interpreter())
