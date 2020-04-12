import sys
from scanner import lexer, find_column
from Mparser import parser
from TreePrinter import TreePrinter

if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    # lexer.input(text)
    # for token in lexer:
    #     # column = find_column(text, token)
    #     # print('(%d,%d): %s(%s)' % (token.lineno, column, token.type, token.value))
    #     print('(%d): %s(%s)' % (token.lineno, token.type, token.value))

    ast = parser.parse(text, lexer=lexer)
    ast.printTree()
