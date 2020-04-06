import pytest
import subprocess
from pathlib import Path


@pytest.mark.parametrize('name, lineno, illegal_character', (
    ('unknown_operator.txt', 3, '&'),
))
def test_error_stdout(name, lineno, illegal_character, capsys):
    """
    Skaner powinien rozpoznawać niepoprawne leksykalnie wejście.
    W takim przypadku powinien zostać wypisany numer niepoprawnej linii wraz z szczegółową informacją o błędzie.
    """
    current_path = Path(__file__).parent
    script_path = current_path.parent / 'scanner.py'
    input_path = current_path / 'resources' / 'error_stdout' / name
    completed = subprocess.run(['python', script_path, input_path], capture_output=True)
    actual_stdout = completed.stdout.decode().replace('\r\n', '\n')

    expected_error_message = "(%d): illegal character '%s'" % (lineno, illegal_character)

    assert expected_error_message in actual_stdout
