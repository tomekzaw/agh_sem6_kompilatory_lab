import pytest
from Mparser import parser
from AST import *


@pytest.mark.parametrize('comp_op', ('<', '>', '<=', '>=', '==', '!='))
def test_condition(comp_op):
    text = f"if (a {comp_op} b) break;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            If(
                Condition(
                    comp_op,
                    Variable('a'),
                    Variable('b')
                ),
                Break()
            )
        ])
    )


def test_condition_is_not_expression():
    text = "foo = a < b;"
    parser.parse(text)
    assert not parser.errorok


def test_condition_nonassoc():
    text = "if (a < b < c) break;"
    parser.parse(text)
    assert not parser.errorok
