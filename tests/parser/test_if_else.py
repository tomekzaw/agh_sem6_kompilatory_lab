from Mparser import parser
from AST import *


def test_if():
    text = "if (a < b) break;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            If(
                Condition(
                    '<',
                    Variable('a'),
                    Variable('b')
                ),
                Break()
            )
        ])
    )


def test_if_else():
    text = "if (a < b) break; else continue;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            If(
                Condition(
                    '<',
                    Variable('a'),
                    Variable('b')
                ),
                Break(),
                Continue()
            )
        ])
    )


def test_nested_if():
    text = """
    if (a < b)
        if (c < d)
            break;
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            If(
                Condition(
                    '<',
                    Variable('a'),
                    Variable('b')
                ),
                If(
                    Condition(
                        '<',
                        Variable('c'),
                        Variable('d')
                    ),
                    Break()
                )
            )
        ])
    )


def test_dangling_else_iiaea():
    text = """
    if (a < b)
    if (c < d)
    break;
    else
    continue;
    """

    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            If(
                Condition('<', Variable('a'), Variable('b')),
                If(
                    Condition('<', Variable('c'), Variable('d')),
                    Break(),
                    Continue()
                )
            )
        ])
    )

    outer_if = ast.instructions.instructions[0]
    inner_if = outer_if.instruction_then
    assert outer_if.instruction_else is None
    assert inner_if.instruction_else is not None


def test_dangling_else_iiaeiaea():
    text = """
    if (a < b)
    if (c < d)
    break;
    else
    if (e < f)
    continue;
    else
    return;
    """

    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            If(
                Condition('<', Variable('a'), Variable('b')),
                If(
                    Condition('<', Variable('c'), Variable('d')),
                    Break(),
                    If(
                        Condition('<', Variable('e'), Variable('f')),
                        Continue(),
                        Return()
                    )
                )
            )
        ])
    )

    if1 = ast.instructions.instructions[0]
    if2 = if1.instruction_then
    if3 = if2.instruction_else

    assert if1.instruction_else is None
    assert if2.instruction_else is not None
    assert if3.instruction_else is not None
