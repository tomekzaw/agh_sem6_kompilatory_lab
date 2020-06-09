import pytest
from utils import typechecker_passes, typechecker_fails


@pytest.mark.parametrize('text', (
    """a = [1, 2, 3][1];""",

    """a = [[1, 2], [3, 4]][1, 4];""",
))
def test_reference_indices_count_passes(text):
    typechecker_passes(text)


@pytest.mark.parametrize('text', (
    """a = [1, 2, 3][];""",
    """a = [1, 2, 3][1, 2];""",

    """a = [[1, 2], [3, 4]][];""",
    """a = [[1, 2], [3, 4]][1];""",
    """a = [[1, 2], [3, 4]][1, 2, 3];""",
    """a = [[1, 2], [3, 4]][1, 2, 3, 4];""",
))
def test_reference_indices_count_fails(text):
    typechecker_fails(text)
