import pytest
from Mparser import parser
from TypeChecker import TypeChecker


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
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert typeChecker.errorok


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
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert not typeChecker.errorok
