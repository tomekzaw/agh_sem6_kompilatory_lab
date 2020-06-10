import pytest
import numpy as np
from Mparser import parser
from scanner import lexer
from Interpreter import Interpreter


@pytest.mark.parametrize('text, expected_value', (
    # BinExpr
    ('6 + 2', 8),
    ('6.0 + 2', 8.0),
    ('6 + 2.0', 8.0),
    ('6.0 + 2.0', 8.0),

    ('6 - 2', 4),
    ('6.0 - 2', 4.0),
    ('6 - 2.0', 4.0),
    ('6.0 - 2.0', 4.0),

    ('6 * 2', 12),
    ('6.0 * 2', 12.0),
    ('6 * 2.0', 12.0),
    ('6.0 * 2.0', 12.0),

    ('6 / 2', 3.0),
    ('6.0 / 2', 3.0),
    ('6 / 2.0', 3.0),
    ('6.0 / 2.0', 3.0),

    ('"Hello" * 0', ''),
    ('"Hello" * 1', 'Hello'),
    ('"Hello" * 3', 'HelloHelloHello'),

    ('[1, 2, 3] .+ [4, 5, 6]', np.array([5, 7, 9])),
    ('[1, 2, 3] .- [4, 5, 6]', np.array([-3, -3, -3])),
    ('[1, 2, 3] .* [4, 5, 6]', np.array([4, 10, 18])),
    ('[1, 2, 3] ./ [4, 5, 6]', np.array([0.25, 0.4, 0.5])),

    ('[[1, 2], [3, 4]] .+ [[5, 6], [7, 8]]', np.array([[6, 8], [10, 12]])),
    ('[[1, 2], [3, 4]] .- [[5, 6], [7, 8]]', np.array([[-4, -4], [-4, -4]])),
    ('[[1, 2], [3, 4]] .* [[5, 6], [7, 8]]', np.array([[5, 12], [21, 32]])),
    ('[[1, 2], [3, 4]] ./ [[5, 6], [7, 8]]', np.array([[0.2, 1/3], [3/7, 0.5]])),

    ('[[1, 2], [3, 4]] * [[0, 1], [2, 3]]', np.array([[4, 7], [8, 15]])),
    ('[[1, 2, 3], [4, 5, 6]] * [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]', np.array([[38, 44, 50, 56], [83, 98, 113, 128]])),

    # UnaryExpr
    ('-42', -42),
    ('-3.14', -3.14),
    ('-[1, 2, 3]', np.array([-1, -2, -3])),
    ('-[[1, 2], [3, 4]]', np.array([[-1, -2], [-3, -4]])),
    ("[[1, 2], [3, 4]]'", np.array([[1, 3], [2, 4]])),
    ("[[1, 2, 3], [4, 5, 6]]'", np.array([[1, 4], [2, 5], [3, 6]])),

    # IntNum
    ('0', 0),
    ('42', 42),

    # FloatNum
    ('0.0', 0.0),
    ('3.14', 3.14),

    # String
    ('""', ''),
    ('"Hello world!"', 'Hello world!'),

    # Vector
    ('[]', np.array([])),
    ('[[]]', np.array([[]])),
    ('[1, 2, 3]', np.array([1, 2, 3])),
    ('[[1, 2], [3, 4]]', np.array([[1, 2], [3, 4]])),

    # matrix special functions
    ('eye(3)', np.eye(3, 3)),
    ('eye(3, 4)', np.eye(3, 4)),
    ('zeros(3)', np.zeros((3, 3))),
    ('zeros(3, 4)', np.zeros((3, 4))),
    ('ones(3)', np.ones((3, 3))),
    ('ones(3, 4)', np.ones((3, 4))),
))
def test_memory_value(text, expected_value):
    text = f'a = {text};'

    ast = parser.parse(text, lexer=lexer)
    interpreter = Interpreter()
    ast.accept(interpreter)

    a = interpreter.memory_stack.stack[0].symbols['a']
    if isinstance(expected_value, np.ndarray):
        assert np.array_equal(a, expected_value)
    else:
        assert a == expected_value
        assert type(a) == type(expected_value)
