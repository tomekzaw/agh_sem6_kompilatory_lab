import pytest
from pathlib import Path
from Mparser import parser


@pytest.mark.parametrize('name', (
    'example1.m',
    'example2.m',
    'example3.m',
))
def test_accept(name):
    input_path = Path(__file__).parent / 'resources' / 'accept' / 'input' / name
    with open(input_path, 'r') as f:
        text = f.read()
    parser.parse(text)
