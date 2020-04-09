import pytest
from Mparser import parser
from ast_ import *


@pytest.mark.parametrize('text', (
    "foo = -123;",
    "foo = - 123;",
))
def test_unary_minus(text):
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                UnaryExpr(
                    '-',
                    IntNum(123)
                )
            )
        ])
    )


@pytest.mark.parametrize('text', (
    "foo = --123;",
    "foo = - -123;",
    "foo = - - 123;",
))
def test_double_unary_minus(text):
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                UnaryExpr(
                    '-',
                    UnaryExpr(
                        '-',
                        IntNum(123)
                    )
                )
            )
        ])
    )


@pytest.mark.parametrize('text', (
    "foo = 123-456;",
    "foo = 123- 456;",
    "foo = 123 -456;",
    "foo = 123 - 456;",
))
def test_unary_vs_binary_minus(text):
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                BinExpr(
                    '-',
                    IntNum(123),
                    IntNum(456)
                )
            )
        ])
    )


@pytest.mark.parametrize('text', (
    "foo = A';",
    "foo = A ';",
))
def test_transpose(text):
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                UnaryExpr(
                    "'",
                    Variable('A')
                )
            )
        ])
    )

@pytest.mark.parametrize('text', (
    "foo = A'';",
    "foo = A' ';",
    "foo = A ' ';",
))
def test_double_transpose(text):
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                UnaryExpr(
                    "'",
                    UnaryExpr(
                        "'",
                        Variable('A')
                    )
                )
            )
        ])
    )
