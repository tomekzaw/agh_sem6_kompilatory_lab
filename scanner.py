#!/usr/bin/python

import sys
import ply.lex as lex

reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    'return': 'RETURN',
    'eye': 'EYE',
    'zeros': 'ZEROS',
    'ones': 'ONES',
    'print': 'PRINT',
}

tokens = [
    'DOTADD',
    'DOTSUB',
    'DOTMUL',
    'DOTDIV',
    'ADDASSIGN',
    'SUBASSIGN',
    'MULASSIGN',
    'DIVASSIGN',
    'LTE',
    'GTE',
    'NEQ',
    'EQ',
    'ID',
    'FLOATNUM',
    'INTNUM',
    'STRING',
] + list(reserved.values())

literals = "+-*/=<>()[]{}:',;"

t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

t_LTE = r'<='
t_GTE = r'>='
t_NEQ = r'!='
t_EQ = r'=='

t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'


def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # or: r'[a-zA-Z_]\w*' for short, since \w also matches underscore (_)
    t.type = reserved.get(t.value, 'ID')
    return t


def t_FLOATNUM(t):
    r'((\d+\.\d*|\.\d+)([eE][-+]?\d+)?|(\d+([eE][-+]?\d+)))'  # allows 1e42
    # or: r'(\d+\.\d*|\.\d+)([eE][-+]?\d+)?' to disallow 1e42
    t.value = float(t.value)
    return t


def t_INTNUM(t):
    r'\d+'  # allows leading zeros
    # or: r'([1-9]\d*|0)' to disallow leading zeros
    t.value = int(t.value)
    return t


def t_STRING(t):
    r'\"(.*?[^\\])??\"'  # for single-line strings, including empty string ("")
    # or: r'\"((.|\n)*?[^\\])??\"' to allow multi-line strings
    # it is also necessary to update line numbering:
    # t.lexer.lineno += t.value.count('\n')
    t.value = t.value[1:-1].replace(r'\"', '"').replace(r"\\", "\\")
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("(%d): illegal character '%s'" % (t.lineno, t.value[0]), file=sys.stderr)
    t.lexer.skip(1)


def find_column(input, token):
    line_start = input.rfind('\n', 0, token.lexpos) + 1
    return (token.lexpos - line_start) + 1


def find_tok_column(token):
    last_cr = lexer.lexdata.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = 0
    return token.lexpos - last_cr


lexer = lex.lex()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    lexer.input(text)
    for token in lexer:
        # column = find_column(text, token)
        # print('(%d,%d): %s(%s)' % (token.lineno, column, token.type, token.value))
        print('(%d): %s(%s)' % (token.lineno, token.type, token.value))
