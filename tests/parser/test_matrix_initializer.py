from Mparser import parser
from AST import *


def test_matrix():
    text = """
    E1 = [ [ 1, 2, 3],
           [ 4, 5, 6],
           [ 7, 8, 9] ];
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Assignment(
                '=',
                Variable('E1'),
                Vector([
                    Vector([IntNum(1), IntNum(2), IntNum(3)]),
                    Vector([IntNum(4), IntNum(5), IntNum(6)]),
                    Vector([IntNum(7), IntNum(8), IntNum(9)])
                ])
            )
        ])
    )
