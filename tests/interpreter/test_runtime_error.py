import pytest
from Mparser import parser
from scanner import lexer
from Interpreter import Interpreter


@pytest.mark.parametrize('text, message', (
    ('A = 0/0;', 'division by zero'),
    ('A = 1/0;', 'division by zero'),

    ('A = "Hello" * -1;', 'negative number'),

    ('A = zeros(1, 4) * ones(5, 1);', 'unmatching shapes'),

    ('A = zeros(3, 4); print A[-1, 2];', 'negative index'),
    ('A = zeros(3, 4); print A[2, -1];', 'negative index'),
    ('A = zeros(3, 4); print A[42, 2];', 'out of bounds'),
    ('A = zeros(3, 4); print A[2, 42];', 'out of bounds'),

    ('A = zeros(3, 4); print A[1];', 'invalid number of indices'),
    ('A = zeros(3, 4); A[1] = 42;', 'invalid number of indices'),
    ('A = [1, 2, 3]; print A[1, 2];', 'invalid number of indices'),
    ('A = [1, 2, 3]; A[1, 2] = 42;', 'invalid number of indices'),

    ('A = eye(-1);', 'negative number of rows'),
    ('A = zeros(-1);', 'negative number of rows'),
    ('A = ones(-1);', 'negative number of rows'),

    ('A = eye(3, -1);', 'negative number of columns'),
    ('A = zeros(3, -1);', 'negative number of columns'),
    ('A = ones(3, -1);', 'negative number of columns'),
))
def test_runtime_error(text, message):
    ast = parser.parse(text, lexer=lexer)
    with pytest.raises(RuntimeError) as excinfo:
        ast.accept(Interpreter(catch_runtime_errors=False))
    assert message in str(excinfo.value)
