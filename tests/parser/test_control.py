import pytest
from Mparser import parser
from ast_ import *


@pytest.mark.parametrize('text, node', (
    ("break;", Break()),
    ("continue;", Continue()),
    ("return;", Return()),
    ("return foo;", Return(Variable('foo'))),
    ("return 42;", Return(IntNum(42))),
    ("return 123 + 456;", Return(BinExpr('+', IntNum(123), IntNum(456)))),
))
def test_control(text, node):
    ast = parser.parse(text)
    assert ast == Program(
        Instructions([
            node
        ])
    )
