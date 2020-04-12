import pytest
from itertools import product
from Mparser import parser
from ast_ import *


def test_expression_group_unary():
    text = "foo = (-A)';"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                UnaryExpr(
                    "'",
                    UnaryExpr(
                        '-',
                        Variable('A')
                    )
                )
            )
        ])
    )


def test_expression_group_binary():
    text = f"foo = (123 + 456) * 789;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                BinExpr(
                    '*',
                    BinExpr(
                        '+',
                        IntNum(123),
                        IntNum(456)
                    ),
                    IntNum(789)
                )
            )
        ])
    )


def test_expression_group_nested():
    text = "foo = (12 + ((34 - 56) * 78)) / 90;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                BinExpr(
                    '/',
                    BinExpr(
                        '+',
                        IntNum(12),
                        BinExpr(
                            '*',
                            BinExpr(
                                '-',
                                IntNum(34),
                                IntNum(56),
                            ),
                            IntNum(78)
                        )
                    ),
                    IntNum(90)
                )
            )
        ])
    )


@pytest.mark.parametrize('n', range(5))
def test_expression_group_nested_multiple(n):
    text = f"foo = {'(' * n}123{')' * n};"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                IntNum(123)
            )
        ])
    )
