import pytest
from Mparser import parser
from TypeChecker import TypeChecker


@pytest.mark.parametrize('text', (
    "foo = 2 + 2;",
    "foo = 2 + 2.0;",

    'foo = "Hello" + " world!";',
    'foo = "Hello!" + "";',

    "foo = [] .+ [];",
    "foo = [ [] ] .+ [ [] ];",

    "foo = [1, 2] .+ [3, 4];",
    "foo = [ [1, 2] ] .+ [ [3, 4] ];",
    "foo = [ [1], [2] ] .+ [ [3], [4] ];",

    """
    foo = [ [1, 2, 3],
            [4, 5, 6] ] .+ [ [ 7, 8, 9],
                             [10,11,12] ];
    """,

    "foo = ones(3, 4) .+ eyes(3, 4);",
))
def test_binary_expression_pass(text):
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert typeChecker.errorok


@pytest.mark.parametrize('text', (
    # dodawanie skalara lub wektora do macierzy
    "foo = [ [1, 2], [3, 4] ] .+ 5;"
    "foo = [ [1, 2], [3, 4] ] .+ [5, 6];"

    # operacje binarne na wektorach lub macierzach o niekompatybilnych wymiarach
    "foo = [ [1, 2] ] .+ [ [3], [4] ];",

    'foo = 2 + "hello";',
))
def test_binary_expression_fail(text):
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert not typeChecker.errorok
