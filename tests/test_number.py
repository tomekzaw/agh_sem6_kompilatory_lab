import pytest
from scanner import lexer


@pytest.mark.parametrize('lexer_input, expected_type, expected_value', (
    # int vs. float
    ('0', 'INTNUM', 0),
    ('0.', 'FLOATNUM', 0),
    ('.0', 'FLOATNUM', 0),
    ('0.0', 'FLOATNUM', 0),
    ('123', 'INTNUM', 123),
    ('123.', 'FLOATNUM', 123.0),
    ('123.0', 'FLOATNUM', 123.0),
    ('.45', 'FLOATNUM', 0.45),
    ('0.45', 'FLOATNUM', 0.45),
    ('1e67', 'FLOATNUM', 1e67),
    ('1E67', 'FLOATNUM', 1e67),
    ('1.e67', 'FLOATNUM', 1e67),
    ('.45e67', 'FLOATNUM', 0.45e67),

    # sign
    ('+0', 'INTNUM', 0),
    ('-0', 'INTNUM', 0),
    ('+123', 'INTNUM', 123),
    ('-123', 'INTNUM', -123),
    ('+123.45', 'FLOATNUM', 123.45),
    ('-123.45', 'FLOATNUM', -123.45),

    # leading zeros
    ('00', 'INTNUM', 0),
    ('0123', 'INTNUM', 123),
    ('000123', 'INTNUM', 123),
    ('0e000', 'FLOATNUM', 0.0),
    ('00.123', 'FLOATNUM', 0.123),
    ('123.45e067', 'FLOATNUM', 123.45e67),
    ('123.45e00067', 'FLOATNUM', 123.45e67),

    # exponent sign
    ('123.45e+67', 'FLOATNUM', 123.45e67),
    ('123.45e-67', 'FLOATNUM', 123.45e-67),
))
def test_valid_number(lexer_input, expected_type, expected_value):
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) == 1
    assert tokens[0].type == expected_type
    assert tokens[0].value == expected_value
    assert type(tokens[0].value) == {'INTNUM': int, 'FLOATNUM': float}[expected_type]


@pytest.mark.parametrize('lexer_input', (
    '',
    '+',
    '-',
    '.',
    'e',
    'e+',
    'e-',
    'E',
    '++123',
    '--123',
    '-+123',
    '+-123',
    '123e',
    '123e+',
    '123e-',
    '123.45e++67',
    '123.45e--67',
    '123.45e+-67',
    '123.45e-+67',
    '123.45e67.89',
    '123.45e+',
    '123.45e-',
    '123.45e.',
    '123.45e.89',
    'e67',
    '.e67',
    'e67E77',
    '1e67E77',
))
def test_invalid_number(lexer_input):
    lexer.input(lexer_input)
    tokens = list(lexer)

    assert len(tokens) != 1 or tokens[0].type not in ('INTNUM', 'FLOATNUM')
