import pytest
from scanner import lexer


@pytest.mark.parametrize('lexer_input, expected_value', (
    (r'""', ""),
    (r'"Hello"', "Hello"),
    (r'"Hello world"', "Hello world"),
    (r'"Hello\tworld"', "Hello\\tworld"),

    (r'"\""', "\""),
    (r'"\"\""', "\"\""),
    (r'"\\\""', "\\\""),
    (r'"\\a"', "\\a"),
    (r'"\\\\a"', "\\\\a"),
    (r'"\"\""', "\"\""),

    (r'"Hello \"world"', "Hello \"world"),
    (r'"Hello \"world\""', "Hello \"world\""),
    (r'"Lorem \"ipsum\" sit \"dolor\" amet"', "Lorem \"ipsum\" sit \"dolor\" amet"),
))
def test_valid_string(lexer_input, expected_value):
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) == 1
    assert tokens[0].type == 'STRING'
    assert tokens[0].value == expected_value


@pytest.mark.parametrize('lexer_input', (
    r'"',
    r'"""',
    r'"\"',
    r'"\"\"',
    r'"\\\"',
    r'"Hello \"',
    r'"Hello \"world\"',
))
def test_invalid_string(lexer_input):
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) != 1 or tokens[0].type != 'STRING' or tokens[0].value != lexer_input
