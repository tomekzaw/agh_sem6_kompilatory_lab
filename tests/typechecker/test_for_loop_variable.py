import pytest
from utils import typechecker_passes, typechecker_fails


def test_loop_variable_cannot_overwrite():
    text = """
    i = 42;
    for i = 1:10 {
        print(i);
    }
    """
    assert typechecker_fails(text)


def test_cannot_assign_to_loop_variable():
    text = """
    for i = 1:10 {
        i = 2;
    }
    """
    assert typechecker_fails(text)


def test_cannot_modify_loop_variable():
    text = """
    for i = 1:10 {
        i += 2;
    }
    """
    assert typechecker_fails(text)


def test_loop_variable_available_only_inside_loop():
    text = """
    for i = 1:10 {
        print(i);
    }
    print(i);
    """
    assert typechecker_fails(text)


def test_outer_loop_variable_as_inner_loop_range():
    text = """
    for i = 1:10 {
        for j = i:10 {
            print(i, j);
        }
    }
    """
    assert typechecker_passes(text)


def test_two_loops_same_variable():
    text = """
    for i = 1:10 {
        for i = 1:10 {
            print(i);
        }
    }
    """
    assert typechecker_fails(text)

