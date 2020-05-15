import pytest
from utils import typechecker_passes, typechecker_fails


@pytest.mark.parametrize('text', (
    "foo = -42;",
    "foo = -42.0;",

    "foo = -[];",
    "foo = -[[]];",
    "foo = -[1];",
    "foo = -[1, 2, 3];",
    "foo = -[ [1] ];",
    "foo = -[ [1, 2, 3] ];",

    "foo = [[]]';",
    "foo = [ [1] ]';",
    "foo = [ [1, 2, 3] ]';",
    "foo = [ [1], [2], [3] ]';",

    "foo = --42;",
    "foo = --42.0;",
    "foo = --[1, 2, 3];",
    "foo = --[ [1, 2, 3] ];",
    "foo = [ [1, 2, 3] ]'';",
))
def test_unary_expression_pass(text):
    assert typechecker_passes(text)


@pytest.mark.parametrize('text', (
    'foo = -"Hello";',

    "foo = []';",
    "foo = [0]';",
    "foo = [0, 0, 0]';",
))
def test_unary_expression_fail(text):
    assert typechecker_fails(text)
