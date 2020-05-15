import pytest
from utils import typechecker_fails


@pytest.mark.parametrize('text', (
    '''
    a = 2;
    b = "hello";
    c = a + b;
    ''',
))
def test_variable_value(text):
    assert typechecker_fails(text)


def test_variable_matrix_different_shape():
    text = '''
    x = eye(5);
    y = eye(8);
    z = x + y;
    '''
    assert typechecker_fails(text)
