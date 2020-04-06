import pytest
from scanner import lexer


@pytest.mark.parametrize('lexer_input', (
    'a',
    'abc',
    'A',
    'ABC',
    '_',
    '___',
    '_abc',
    '_abc_',
    'abc_',
    '_abc_DEF',
    'e42',
    'E42',
    '_1e42',
    '_1E42',
))
def test_valid_identifier(lexer_input):
    """
    pierwszy znak identyfikatora to litera lub znak _, w kolejnych znakach mogą dodatkowo wystąpić cyfry
    """
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) == 1
    assert tokens[0].type == 'ID'
    assert tokens[0].value == lexer_input


@pytest.mark.parametrize('lexer_input', (
    '',
    'abc def',
    'abc.def',
    'abc-def',
    '42',
    '+42',
    '-42',
    '1e42',
    '_+',
))
def test_invalid_identifier(lexer_input):
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) != 1 or tokens[0].type != 'ID' or tokens[0].value != lexer_input
