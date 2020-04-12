import pytest
from Mparser import parser
from ast_ import *


@pytest.mark.parametrize('function, node_type', (
    ('zeros', Zeros),
    ('ones', Ones),
    ('eye', Eye),
))
@pytest.mark.parametrize('argc', (1, 2))
def test_matrix_function(function, node_type, argc):
    args = ', '.join(['42'] * argc)
    text = f"foo = {function}({args});"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('foo'),
                node_type(*[IntNum(42) for _ in range(argc)])
            )
        ])
    )
