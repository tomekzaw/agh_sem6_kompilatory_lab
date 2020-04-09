import pytest
from Mparser import parser
from ast_ import *


@pytest.mark.parametrize('ass_op', ('=', '+=', '-=', '*=', '/='))
def test_assignment_to_variable(ass_op):
    text = f"foo {ass_op} 42;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                ass_op,
                Variable('foo'),
                IntNum(42)
            )
        ])
    )


@pytest.mark.parametrize('ass_op', ('=', '+=', '-=', '*=', '/='))
def test_assignment_to_matrix_index(ass_op):
    text = f"A[1, 2] {ass_op} 42;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                ass_op,
                MatrixElement(
                    Variable('A'),
                    IntNum(1),
                    IntNum(2)
                ),
                IntNum(42)
            )
        ])
    )

@pytest.mark.parametrize('expression', (
    "42",
    "42.0",
    "\"Hello world!\"",
    "-A",
    "A'",
    "(A)",
    "A+B",
    "1:10",
    "[1, 2; 3, 4]",
    "[1, 2; 3, 4][1, 2]",
    "zeros(5)",
    "ones(7)",
    "eye(10)",
))
@pytest.mark.parametrize('ass_op', ('=', '+=', '-=', '*=', '/='))
def test_assignment_to_expression(expression, ass_op):
    text = f"{expression} {ass_op} 42;"
    with pytest.raises(SystemExit):
        parser.parse(text)
