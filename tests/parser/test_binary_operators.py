import pytest
from itertools import chain, product
from Mparser import parser
from ast_ import *


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


@pytest.mark.parametrize('op1, op2', chain(
    product(('+', '-', '.+', '.-'), repeat=2),
    product(('*', '/', '.*', './'), repeat=2),
))
def test_left_associativity(op1, op2):
    text = f"foo = 123 {op1} 456 {op2} 789;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                BinExpr(
                    op2,
                    BinExpr(
                        op1,
                        IntNum(123),
                        IntNum(456)
                    ),
                    IntNum(789)
                )
            )
        ])
    )


@pytest.mark.parametrize('op1, op2', product(('+', '-', '*', '/', '.+', '.-', '.*', './'), repeat=2))
def test_expression_group(op1, op2):
    text = f"foo = (123 {op1} 456) {op2} 789;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                BinExpr(
                    op2,
                    BinExpr(
                        op1,
                        IntNum(123),
                        IntNum(456)
                    ),
                    IntNum(789)
                )
            )
        ])
    )
