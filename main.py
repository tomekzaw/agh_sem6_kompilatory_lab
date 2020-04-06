import sys
from scanner import lexer, find_column

if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else 'example_full.txt'
    with open(path, 'r') as f:
        text = f.read()

    lexer.input(text)
    for token in lexer:
        # column = find_column(text, token)
        # print('(%d,%d): %s(%s)' % (token.lineno, column, token.type, token.value))
        print('(%d): %s(%s)' % (token.lineno, token.type, token.value))
