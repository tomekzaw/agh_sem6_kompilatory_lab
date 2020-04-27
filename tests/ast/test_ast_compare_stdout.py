import pytest
import subprocess
from pathlib import Path


@pytest.mark.parametrize('input_name, expected_output_name', (
    ('example.txt', 'example.txt'),
    ('example1.m', 'example1.tree'),
    ('example2.m', 'example2.tree'),
    ('example3.m', 'example3.tree'),
))
def test_compare_stdout(input_name, expected_output_name, capsys):
    """
    Przykładowe pliki wejściowe: example1.m, example2.m, example3.m
    oraz odpowiadające wyjściowe drzewa składni: example1.tree, example2.tree, example3.tree
    """
    current_path = Path(__file__).parent

    script_path = current_path.parent.parent / 'Mparser.py'
    input_path = current_path / 'resources' / 'compare_stdout' / 'input' / input_name
    completed = subprocess.run(['python', script_path, input_path], capture_output=True)
    actual_stdout = completed.stdout.decode().replace('\r\n', '\n')

    expected_output_path = current_path / 'resources' / 'compare_stdout' / 'expected_output' / expected_output_name
    with open(expected_output_path, 'r') as f:
        expected_stdout = f.read().replace('\r\n', '\n')

    assert actual_stdout == expected_stdout
