import pytest
from Mparser import parser
from TypeChecker import TypeChecker


@pytest.mark.parametrize('text', (
    "while (2 + 2 == 4) break;",
    "while (2 + 2 == 4) { break; }",

    "while (2 + 2 == 4) continue;",
    "while (2 + 2 == 4) { continue; }",

    """
    for i = 1:10 {
        while (i < 10) {
            i += 1;
            continue;
        }
        break;
    }
    """,
))
def test_break_continue_pass(text):
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert typeChecker.errorok


@pytest.mark.parametrize('text', (
    # niepoprawne użycie instrukcji break lub continue poza pętlą
    "break;",
    "if (2 + 2 == 4) break;",
    "if (2 + 2 == 4) { break; }",

    "continue;",
    "if (2 + 2 == 4) continue;",
    "if (2 + 2 == 4) { continue; }",

    """
    a = 2;
    b = 3;
    while (a != b) {
        a += 1;
    }
    break;
    c = 4;
    """,
))
def test_break_continue_fail(text):
    ast = parser.parse(text)
    typeChecker = TypeChecker()
    typeChecker.visit(ast)
    assert not typeChecker.errorok
