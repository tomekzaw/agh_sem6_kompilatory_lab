import pytest
from Mparser import parser
from ast_ import *


def test_precedence_transpose_over_unary_minus():
    text = "foo = -A';"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                UnaryExpr(
                    '-',
                    UnaryExpr(
                        "'",
                        Variable('A')
                    )
                )
            )
        ])
    )


@pytest.mark.parametrize('add_op', ('+', '-', '.+', '.-'))
@pytest.mark.parametrize('mul_op', ('*', '/', '.*', './'))
def test_precedence_mul_op_over_add_op(add_op, mul_op):
    text = f"foo = 123 {add_op} 456 {mul_op} 789;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                BinExpr(
                    add_op,
                    IntNum(123),
                    BinExpr(
                        mul_op,
                        IntNum(456),
                        IntNum(789)
                    )
                )
            )
        ])
    )


@pytest.mark.parametrize('expr_op', ('+', '-', '*', '/', '.+', '.-', '.*', './'))
@pytest.mark.parametrize('comp_op', ('<', '>', '<=', '>=', '==', '!='))
def test_precedence_expression_op_over_comparision_op(expr_op, comp_op):
    text = f"if (a {expr_op} b {comp_op} c {expr_op} d) break;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            If(
                Condition(
                    comp_op,
                    BinExpr(
                        expr_op,
                        Variable('a'),
                        Variable('b')
                    ),
                    BinExpr(
                        expr_op,
                        Variable('c'),
                        Variable('d')
                    )
                ),
                Break()
            )
        ])
    )
