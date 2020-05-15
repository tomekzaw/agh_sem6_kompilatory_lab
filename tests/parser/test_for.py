from Mparser import parser
from AST import *


def test_for():
    text = """
    for i = 1:10
        print i;
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            For(
                Variable('i'),
                Range(
                    IntNum(1),
                    IntNum(10),
                ),
                Print([
                    Variable('i')
                ])
            )
        ])
    )


def test_nested_for():
    text = """
    for i = 1:10
        for j = 1:10
            print i, j;
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            For(
                Variable('i'),
                Range(
                    IntNum(1),
                    IntNum(10),
                ),
                For(
                    Variable('j'),
                    Range(
                        IntNum(1),
                        IntNum(10)
                    ),
                    Print([
                        Variable('i'),
                        Variable('j')
                    ])
                )
            )
        ])
    )


def test_for_range_expression():
    text = """
    for i = 2+3*5 : n*n
        print i;
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            For(
                Variable('i'),
                Range(
                    BinExpr(
                        '+',
                        IntNum(2),
                        BinExpr(
                            '*',
                            IntNum(3),
                            IntNum(5)
                        )
                    ),
                    BinExpr(
                        '*',
                        Variable('n'),
                        Variable('n')
                    )
                ),
                Print([
                    Variable('i')
                ])
            )
        ])
    )
