import pytest
from itertools import chain, product
from Mparser import parser
from ast_ import *


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
