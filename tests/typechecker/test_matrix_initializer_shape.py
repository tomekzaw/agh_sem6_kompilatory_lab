import pytest
from utils import typechecker_passes, typechecker_fails


@pytest.mark.parametrize('text', (
    "X = [];",
    "X = [ [] ];",
    "X = [ [], [] ];",

    "X = [1];",
    "X = [1, 2, 3];",

    "X = [ [1] ];",
    "X = [ [1, 2, 3] ];",

    """
    x = [ [1, 2, 3, 4],
          [5, 6, 7, 8],
          [9,10,11,12] ];
    """,
))
def test_matrix_initializer_shape_pass(text):
    assert typechecker_passes(text)


@pytest.mark.parametrize('text', (
    "X = [ [ [] ] ];",
    "X = [ [ [0] ] ];",
    "X = [ [ [ [] ] ] ];",
    "X = [ [], [ [] ] ];",
    "X = [ [ [] ], [] ];",
    "X = [ [ [] ], [ [] ] ];",

    # inicjalizacja macierzy przy użyciu wektorów o różnych rozmiarach
    "X = [ [], [0] ];",
    "X = [ [0], [] ];",
    "X = [ [0], [0, 0] ];",
    "X = [ [0, 0], [0] ];",

    """
    x = [ [1, 2, 3],
          [1, 2, 3, 4, 5],
          [1, 2] ];
    """,
))
def test_matrix_initializer_shape_fail(text):
    assert typechecker_fails(text)
