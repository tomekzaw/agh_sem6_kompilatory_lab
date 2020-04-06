import pytest
from scanner import lexer


def test_1e42_is_floatnum():
    lexer_input = '1e42'
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) == 1
    assert tokens[0].type == 'FLOATNUM'
    assert tokens[0].value == 1e42


def test_hash_in_string():
    lexer_input = r'"Hello #world"'
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) == 1
    assert tokens[0].type == 'STRING'
    assert tokens[0].value == "Hello #world"


@pytest.mark.parametrize('lexer_input', (
    '1.+2',
    '1.-2',
    '1.*2',
    '1./2',
))
def test_digit_dot_op_digit(lexer_input):
    """
    (1)(.+)(2) vs. (1.)(+)(2) vs. (1.)(+2)
    """
    lexer.input(lexer_input)
    tokens = list(lexer)

    pass  # no requirements specified


@pytest.mark.parametrize('reserved_word', (
    'if',
    'else',
    'for',
    'while',
    'break',
    'continue',
    'return',
    'eye',
    'zeros',
    'ones',
    'print',
))
def test_reserved_word_is_not_identifier(reserved_word):
    lexer.input(reserved_word)
    tokens = list(lexer)

    assert len(tokens) == 1
    assert tokens[0].type == reserved_word.upper()


@pytest.mark.parametrize('identifier', (
    'forget',
    'printed',
))
def test_identifier_prefix_reserved_word(identifier):
    lexer.input(identifier)
    tokens = list(lexer)

    assert len(tokens) == 1
    assert tokens[0].type == 'ID'
    assert tokens[0].value == identifier
