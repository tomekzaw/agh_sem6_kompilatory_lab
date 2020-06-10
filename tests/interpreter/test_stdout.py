import pytest
import numpy as np
from Mparser import parser
from scanner import lexer
from Interpreter import Interpreter


@pytest.mark.parametrize('text, expected_stdout', (
    # print
    ('print "Hello world!";', 'Hello world!\n'),
    ('print;', '\n'),
    ('print 2+2;', '4\n'),
    ('print 1*1, 2*2, 3*3;', '1, 4, 9\n'),

    # break/continue in for/while
    (
        """
        for i = 1:10 {
            if (i == 5) {
                continue;
            }
            print(i);
            if (i == 8) {
                break;
            }
        }
        """,
        '1\n2\n3\n4\n6\n7\n8\n'
    ),
    (
        """
        i = 1;
        while (i <= 10) {
            if (i == 5) {
                i = i + 1;
                continue;
            }
            print(i);
            if (i == 8) {
                break;
            }
            i = i + 1;
        }
        """,
        '1\n2\n3\n4\n6\n7\n8\n'
    ),

    # compound assignments
    (
        """
        a = 3;
        a += 2;
        print a;
        """,
        '5\n'
    ),
    (
        """
        a = [1, 2, 3];
        a += 4;
        print a;
        """,
        '[5 6 7]\n'
    ),
    (
        """
        a = [1, 2, 3];
        a += [4, 5, 6];
        print a;
        """,
        '[5 7 9]\n'
    ),
))
def test_compare_stdout(text, expected_stdout, capsys):
    ast = parser.parse(text, lexer=lexer)
    ast.accept(Interpreter())
    captured = capsys.readouterr()
    assert captured.out == expected_stdout
