import pytest
from scanner import lexer


@pytest.mark.parametrize('lexer_input, token_name', (
    # operatory binarne: +, -, *, /
    ('+', '+'),
    ('-', '-'),
    ('*', '*'),
    ('/', '/'),

    # macierzowe operatory binarne (dla operacji element po elemencie): .+, .-, .*, ./
    ('.+', 'DOTADD'),
    ('.-', 'DOTSUB'),
    ('.*', 'DOTMUL'),
    ('./', 'DOTDIV'),

    # operatory przypisania: =, +=, -=, *=, /=
    ('=', '='),
    ('+=', 'ADDASSIGN'),
    ('-=', 'SUBASSIGN'),
    ('*=', 'MULASSIGN'),
    ('/=', 'DIVASSIGN'),

    # operatory relacyjne: <, >, <=, >=, !=, ==
    ('<', '<'),
    ('>', '>'),
    ('<=', 'LTE'),
    ('>=', 'GTE'),
    ('!=', 'NEQ'),
    ('==', 'EQ'),

    # nawiasy: (,), [,], {,}
    ('(', '('),
    (')', ')'),
    ('[', '['),
    (']', ']'),
    ('{', '{'),
    ('}', '}'),

    # operator zakresu: :
    (':', ':'),

    # transpozycja macierzy: '
    ("'", "'"),

    # przecinek i średnik: , ;
    (',', ','),
    (';', ';'),

    # słowa kluczowe: if, else, for, while
    ('if', 'IF'),
    ('else', 'ELSE'),
    ('for', 'FOR'),
    ('while', 'WHILE'),

    # słowa kluczowe: break, continue oraz return
    ('break', 'BREAK'),
    ('continue', 'CONTINUE'),
    ('return', 'RETURN'),

    # słowa kluczowe: eye, zeros oraz ones
    ('eye', 'EYE'),
    ('zeros', 'ZEROS'),
    ('ones', 'ONES'),

    # słowa kluczowe: print
    ('print', 'PRINT'),
))
def test_token(lexer_input, token_name):
    """
    Analizator leksykalny powinien rozpoznawać następujące leksemy:
    * operatory binare: +, -, *, /
    * macierzowe operatory binarne (dla operacji element po elemencie): .+, .-, .*, ./
    * operatory przypisania: =, +=, -=, *=, /=
    * operatory relacyjne: <, >, <=, >=, !=, ==
    * nawiasy: (,), [,], {,}
    * operator zakresu: :
    * transpozycja macierzy: '
    * przecinek i średnik: , ;
    * słowa kluczowe: if, else, for, while
    * słowa kluczowe: break, continue oraz return
    * słowa kluczowe: eye, zeros oraz ones
    * słowa kluczowe: print
    """
    lexer.input(lexer_input)
    token = next(lexer)

    assert token.type == token_name
    assert token.value == lexer_input
