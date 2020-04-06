import pytest
from scanner import lexer


@pytest.mark.parametrize('lexer_input, expected_number_of_tokens', (
    # białe znaki: spacje, tabulatory, znaki nowej linii
    (' ', 0),
    ('   ', 0),
    ('\t', 0),
    ('\t\t\t', 0),
    ('\t \t', 0),

    # komentarze: komentarze rozpoczynające się znakiem # do znaku końca linii
    ('#', 0),
    ('# comment', 0),
    ('# Zażółć gęślą jaźń', 0),
    ('# Hello world', 0),
    ('1 # Hello world', 1),
    ('1 2 3 # Hello world', 3),
    ('# comment # another comment', 0),
    ('# comment\n1 2 3', 3),
    ('# comment\n# comment\n1 2 3', 3),

    ('1 2\t3 # comment', 3),
))
def test_ignored(lexer_input, expected_number_of_tokens):
    """
    Następujące znaki powinny być pomijane:
    * białe znaki: spacje, tabulatory, znaki nowej linii
    * komentarze: komentarze rozpoczynające się znakiem # do znaku końca linii
    """
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) == expected_number_of_tokens
