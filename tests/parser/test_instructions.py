from Mparser import parser
from ast_ import *


def test_empty_program():
    text = ""
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([])
    )


def test_single_instruction():
    text = "break;"
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Break()
        ])
    )


def test_multiple_instructions():
    text = """
    break;
    continue;
    return;
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Break(),
            Continue(),
            Return()
        ])
    )


def test_instructions_blocks():
    text = """
    {
        {
            break;
            {
                {

                }
            }
        }
        continue;
    }
    {

    }
    """
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            Instructions([
                Instructions([
                    Break(),
                    Instructions([
                        Instructions([])
                    ]),
                ]),
                Continue()
            ]),
            Instructions([])
        ])
    )
