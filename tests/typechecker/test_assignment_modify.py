import pytest
from itertools import combinations
from utils import typechecker_passes, typechecker_fails


@pytest.mark.parametrize('value1, value2', combinations((
    '2',
    '3.0',
    '"hello"',
    '[1, 2, 3]',
    '[[1, 2], [3, 4]]',
), 2))
def test_cannot_overwrite_with_other_type(value1, value2):
    text = f"""
    a = {value1};
    a = {value2};
    """
    assert typechecker_fails(text)


@pytest.mark.parametrize('value1, value2', (
    ('2', '3'),
    ('3.0', '3.1'),
    ('"hello"', '"hi"'),
    ('[1, 2, 3]', '[4, 5, 6]'),
    ('[[1, 2], [3, 4]]', '[[5, 6], [7, 8]]'),
))
def test_cannot_overwrite_with_same_type_but_different_value(value1, value2):
    text = f"""
    a = {value1};
    a = {value2};
    """
    assert typechecker_fails(text)


@pytest.mark.parametrize('value', ('2', '3.0', '"hello"', '[1, 2, 3]', '[[1, 2], [3, 4]]'))
def test_cannot_overwrite_with_same_type_and_value(value):
    text = f"""
    a = {value};
    a = {value};
    """
    assert typechecker_fails(text)


@pytest.mark.parametrize('value1, value2', (
    ('2', '3'),
    ('3.0', '3.1'),
    ('"hello"', '"hi"'),
    ('[1, 2, 3]', '[4, 5, 6]'),
    ('[[1, 2], [3, 4]]', '[[5, 6], [7, 8]]'),
))
def test_cannot_overwrite_value_in_if(value1, value2):
    text = f"""
    a = {value1};
    if (1 == 1) {{
        a = {value2};
    }}
    """
    assert typechecker_fails(text)


@pytest.mark.parametrize('text', (
    """
    a = 2;
    if (2 + 2 == 5) {
        a = 3;
    }
    """,

    """
    a = 2;
    for i = 0:-1 {
        a = 3;
    }
    """,

    """
    a = 2;
    while (2 + 2 == 4) {
        break;
        a = 3;
    }
    """,
))
def test_cannot_overwrite_value_even_in_dead_code(text):
    assert typechecker_fails(text)


@pytest.mark.parametrize('initial_value, modifier', (
    ('2', '3'),
    ('3.0', '3.1'),
    ('"hello"', '"hi"'),
    ('[1, 2, 3]', '[4, 5, 6]'),
))
def test_can_modify_value(initial_value, modifier):
    text = f"""
    a = {initial_value};
    a += {modifier};
    """
    assert typechecker_passes(text)


@pytest.mark.parametrize('initial_value, modifier', (
    ('2', '"hi"'),
    ('2', '"3.0"'),
    ('2', '"[1, 2, 3]"'),
    ('2', '"[[1, 2], [3, 4]]"'),
    ('3.0', '"hi"'),
    ('3.0', '"[1, 2, 3]"'),
    ('3.0', '"[[1, 2], [3, 4]]"'),
    ('[1, 2, 3]', '"hi"'),
    ('[1, 2, 3]', '"[[1, 2], [3, 4]]"'),
    ('[[1, 2], [3, 4]]', '"hi"'),
))
def test_cannot_modify_value(initial_value, modifier):
    text = f"""
    a = {initial_value};
    a += {modifier};
    """
    assert typechecker_fails(text)
