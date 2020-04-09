import pytest
from Mparser import parser
from ast_ import *


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
    inner_if = outer_if.instruction_if
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
    if2 = if1.instruction_if
    if3 = if2.instruction_else

    assert if1.instruction_else is None
    assert if2.instruction_else is not None
    assert if3.instruction_else is not None


def test_if_no_instruction():
    text = "if (a < b)"
    with pytest.raises(SystemExit):
        parser.parse(text)


def test_if_empty_instruction():
    text = "if (a < b);"
    ast = parser.parse(text)
    if_ = ast.instructions.instructions[0]
    assert if_.instruction_if == EmptyInstruction()
