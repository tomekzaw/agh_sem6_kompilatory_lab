import pytest
from Mparser import parser
from ast_ import *


def test_print():
    text = "print;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Print([])
        ])
    )


def test_print_string():
    text = 'print "Hello world!";'
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Print([
                String('Hello world!')
            ])
        ])
    )


def test_print_pair():
    text = "print i, j;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Print([
                Variable('i'),
                Variable('j')
            ])
        ])
    )


@pytest.mark.parametrize('n', range(1, 5))
def test_print_expression_list(n):
    text = f"print {', '.join(map(str, range(n)))};"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Print([IntNum(i) for i in range(n)])
        ])
    )
