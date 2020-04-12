import pytest
from Mparser import parser
from ast_ import *


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
    with pytest.raises(SystemExit):
        parser.parse(text)


def test_condition_nonassoc():
    text = "if (a < b < c) break;"
    with pytest.raises(SystemExit):
        parser.parse(text)
