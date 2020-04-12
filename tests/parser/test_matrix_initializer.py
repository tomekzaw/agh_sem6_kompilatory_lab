import pytest
from Mparser import parser
from ast_ import *


def test_empty_matrix():
    text = "E1 = [];"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('E1'),
                Matrix([[]])
            )
        ])
    )


def test_single_element_matrix():
    text = "E1 = [1];"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('E1'),
                Matrix([
                    [IntNum(1)]
                ])
            )
        ])
    )


def test_single_row_matrix():
    text = "E1 = [1, 2, 3];"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('E1'),
                Matrix([
                    [IntNum(1), IntNum(2), IntNum(3)]
                ])
            )
        ])
    )


def test_full_matrix():
    text = """
    E1 = [ 1, 2, 3;
           4, 5, 6;
           7, 8, 9 ] ;
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('E1'),
                Matrix([
                    [IntNum(1), IntNum(2), IntNum(3)],
                    [IntNum(4), IntNum(5), IntNum(6)],
                    [IntNum(7), IntNum(8), IntNum(9)]
                ])
            )
        ])
    )
