import pytest
from Mparser import parser
from AST import *


@pytest.mark.parametrize('assign_op', ('=', '+=', '-=', '*=', '/='))
def test_assignment_to_variable(assign_op):
    text = f"foo {assign_op} 42;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                assign_op,
                Variable('foo'),
                IntNum(42)
            )
        ])
    )


@pytest.mark.parametrize('indices, node', (
    ('1', [IntNum(1)]),
    ('foo', [Variable('foo')]),
    ('1:2', [Range(IntNum(1), IntNum(2))]),
    ('1:i', [Range(IntNum(1), Variable('i'))]),
    ('1:2+3', [Range(IntNum(1), BinExpr('+', IntNum(2), IntNum(3)))]),
    ('i+1:2*j', [Range(BinExpr('+', Variable('i'), IntNum(1)), BinExpr('*', IntNum(2), Variable('j')))]),

    ('1, 2', [IntNum(1), IntNum(2)]),
    ('foo, 2', [Variable('foo'), IntNum(2)]),
    ('1:2, 3', [Range(IntNum(1), IntNum(2)), IntNum(3)]),
    ('1, 2:3', [IntNum(1), Range(IntNum(2), IntNum(3))]),
    ('1:i, j', [Range(IntNum(1), Variable('i')), Variable('j')]),
    ('1:2, 3:4+5', [Range(IntNum(1), IntNum(2)), Range(IntNum(3), BinExpr('+', IntNum(4), IntNum(5)))]),
))
def test_assignment_to_matrix_index(indices, node):
    text = f"A[{indices}] = 42;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Reference(
                    Variable('A'),
                    node
                ),
                IntNum(42)
            )
        ])
    )


@pytest.mark.parametrize('expression', (
    "",
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
    parser.parse(text)
    assert not parser.errorok
