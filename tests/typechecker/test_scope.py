import pytest
from itertools import combinations
from utils import typechecker_passes, typechecker_fails


@pytest.mark.parametrize('text', (
    """
    {
        a = 2;
    }
    print(a);
    """,

    """
    if (1 == 1) a = 2;
    print(a);
    """,

    """
    if (1 == 1) {} else a = 2;
    print(a);
    """,

    """
    if (1 == 1) a = 2; else a = 2;
    print(a);
    """,
))
def test_variable_available_outside_control_statement(text):
    assert typechecker_passes(text)


@pytest.mark.parametrize('text', (
    """
    for i = 1:10
        a = 2;
    print(a);
    """,

    """
    while (1 == 1) a = 2;
    print(a);
    """,
))
def test_local_variable_not_available_in_outer_scope(text):
    assert typechecker_fails(text)


@pytest.mark.parametrize('text', (
    """
    a = 2;
    {
        print(a);
    }
    """,

    """
    a = 2;
    if (1 == 1) print(a);
    """,

    """
    a = 2;
    if (1 == 1) {} else print(a);
    """,

    """
    a = 2;
    if (1 == 1) print(a); else print(a);
    """,

    """
    a = 2;
    for i = 1:10 print(a);
    """,

    """
    a = 2;
    while (1 == 1) print(a);
    """,

    """
    a = 2;
    {
        if (1 == 1) {
            if (1 == 1) {

            } else {
                for i = 1:10 {
                    while (1 == 1) {
                        print(a);
                    }
                }
            }
        }
    }
    """,
))
def test_outer_scope_variables_available_in_local_scope(text):
    assert typechecker_passes(text)


def test_multiple_scopes():
    text = """
    a = 2;
    {
        if (1 == 1) {
            for i = 1:10 {
                while (1 == 1) {
                    print(a);
                }
            }
        }
    }
    """
    assert typechecker_passes(text)


@pytest.mark.parametrize('value1, value2', combinations((
    '2',
    '3.0',
    '"hello"',
    '[1, 2, 3]',
    '[[1, 2], [3, 4]]',
), 2))
def test_if_else_symbol_types_merge_conflict(value1, value2):
    text = f"""
    if (1 == 1)
        a = {value1};
    else
        a = {value2};
    """
    assert typechecker_fails(text)
