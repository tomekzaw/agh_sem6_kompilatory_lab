import pytest
from utils import typechecker_passes, typechecker_fails


@pytest.mark.parametrize('text', (
    "X = zeros(0);",
    "X = zeros(3);",
    "X = zeros(3, 4);",

    """
    n = 3;
    X = zeros(n);
    """,

    """
    m = 2;
    n = 3;
    X = zeros(m, n);
    """,

    """
    A = [1, 2, 3];
    X = zeros(A[1]);
    """,

    """
    A = ones(3)
    X = zeros(A[1, 3]);
    """,
))
def test_matrix_functions_args_pass(text):
    assert typechecker_passes(text)


@pytest.mark.parametrize('text', (
    "X = zeros(3.0);",
    "X = zeros(3.0, 4);",
    "X = zeros(3.0, 4.0);",

    'X = zeros("Hello world!");',
    '''
    string = "Hello world!";
    X = zeros(string);
    ''',

    "X = zeros([3]);",
    '''
    vector = [3];
    X = zeros(vector);
    ''',

    "X = zeros([[3]]);",
    '''
    matrix = [[3]];
    X = zeros(matrix);
    ''',
))
def test_matrix_functions_args_fail(text):
    assert typechecker_fails(text)


# @pytest.mark.parametrize('text', (
#     "X = eye(-1);",

#     """
#     n = -1;
#     X = eye(n);
#     """
# ))
# def test_matrix_function_args_negative(text):
#     assert typechecker_fails(text)
