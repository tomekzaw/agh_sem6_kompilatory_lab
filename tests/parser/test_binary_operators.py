import pytest
from Mparser import parser
from AST import *


@pytest.mark.parametrize('op', ('+', '-', '.+', '.-', '*', '/', '.*', './'))
def test_binary_operator(op):
    text = f"foo = 123 {op} 456;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                BinExpr(
                    op,
                    IntNum(123),
                    IntNum(456)
                )
            )
        ])
    )
