from Mparser import parser
from AST import *


def test_while():
    text = "while (i > 0) break;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            While(
                Condition(
                    '>',
                    Variable('i'),
                    IntNum(0)
                ),
                Break()
            )
        ])
    )


def test_nested_while():
    text = """
    while (i > 0)
        while (j > 0)
            break;
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            While(
                Condition(
                    '>',
                    Variable('i'),
                    IntNum(0)
                ),
                While(
                    Condition(
                        '>',
                        Variable('j'),
                        IntNum(0)
                    ),
                    Break()
                )
            )
        ])
    )
