import pytest
from Mparser import parser
from TypeChecker import TypeChecker


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
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert typeChecker.errorok


@pytest.mark.parametrize('text', (
    'foo = -"Hello";',

    "foo = []';",
    "foo = [0]';",
    "foo = [0, 0, 0]';",
))
def test_unary_expression_fail(text):
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert not typeChecker.errorok
