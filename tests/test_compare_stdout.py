import pytest
import subprocess
from pathlib import Path


@pytest.mark.parametrize('name', (
    'example.txt',
    'example_full.txt',
    'example1.m',
    'example2.m',
    'example3.m',
))
def test_compare_stdout(name, capsys):
    """
    Dla rozpoznanych leksemów stworzony skaner powinien zwracać:
    * odpowiadający token
    * rozpoznany leksem
    * numer linii
    """
    current_path = Path(__file__).parent

    script_path = current_path.parent / 'scanner.py'
    input_path = current_path / 'resources' / 'compare_stdout' / 'input' / name
    completed = subprocess.run(['python', script_path, input_path], capture_output=True)
    actual_stdout = completed.stdout.decode().replace('\r\n', '\n')

    expected_output_path = current_path / 'resources' / 'compare_stdout' / 'expected_output' / name
    with open(expected_output_path, 'r') as f:
        expected_stdout = f.read().replace('\r\n', '\n')

    assert actual_stdout == expected_stdout
