import pytest
from Mparser import parser
from TypeChecker import TypeChecker


@pytest.mark.parametrize('text', (
    "X = zeros(0);",
    "X = zeros(3);",
    "X = zeros(3, 4);",

    "X = zeros(n);",
    "X = zeros(m, n);",

    "X = zeros(A[1]);",
    "X = zeros(A[1, 3]);",
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

    'X = zeros("3");',

    "X = zeros([3]);",

    "X = zeros([[3]]);",
))
def test_matrix_functions_args_fail(text):
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert not typeChecker.errorok
