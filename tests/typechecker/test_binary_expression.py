import pytest
from utils import typechecker_passes, typechecker_fails


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

    "foo = 2 + 3.0;",

    "foo = ones(3, 4) .+ eye(3, 4);",
))
def test_binary_expression_pass(text):
    assert typechecker_passes(text)


@pytest.mark.parametrize('text', (
    # dodawanie skalara lub wektora do macierzy
    "foo = [ [1, 2], [3, 4] ] .+ 5;",
    "foo = [ [1, 2], [3, 4] ] .+ [5, 6];",

    # operacje binarne na wektorach lub macierzach o niekompatybilnych wymiarach
    "foo = [ [1, 2] ] .+ [ [3], [4] ];",

    'foo = 2 + "hello";',
    '''
    a = 2;
    b = "hello";
    foo = a + b;
    ''',

    "foo = ones(3, 4) .+ eye(5, 6);",

    """
    A = ones(3, 4);
    B = eye(5, 6);
    foo = A .+ B;
    """,
))
def test_binary_expression_fail(text):
    assert typechecker_fails(text)
