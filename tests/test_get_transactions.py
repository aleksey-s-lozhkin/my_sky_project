import pytest
from unittest.mock import patch

from src.get_transactions import get_transactions_from_file, get_file_by_drag_and_drop


@patch('src.get_transactions.open_json_transactions')
@patch('src.get_transactions.read_transactions_from_csv')
@patch('src.get_transactions.read_transactions_from_excel')
def test_get_transactions_from_file(mock_excel, mock_csv, mock_json):

    test_filename = 'transaction.smth'
    mock_excel.return_value = [{'file':'excel'}]
    mock_csv.return_value = [{'file':'csv'}]
    mock_json.return_value = [{'file':'json'}]

    mock_excel.side_effect = None
    mock_csv.side_effect = None
    mock_json.side_effect = None

    result1 = get_transactions_from_file('1',test_filename)
    assert result1 == [{'file':'json'}]

    result2 = get_transactions_from_file('2',test_filename)
    assert result2 == [{'file':'csv'}]

    result3 = get_transactions_from_file('3',test_filename)
    assert result3 == [{'file':'excel'}]


@patch('src.get_transactions.open_json_transactions')
@patch('src.get_transactions.read_transactions_from_csv')
@patch('src.get_transactions.read_transactions_from_excel')
def test_get_transactions_from_file_exception(mock_excel, mock_csv, mock_json):

    test_filename = 'transaction.smth'
    mock_excel.return_value = [{'file':'excel'}]
    mock_csv.return_value = [{'file':'csv'}]
    mock_json.return_value = [{'file':'json'}]

    mock_excel.side_effect = FileNotFoundError
    mock_csv.side_effect = FileNotFoundError
    mock_json.side_effect = FileNotFoundError

    result1 = get_transactions_from_file('1', test_filename)
    assert result1 is None

    result2 = get_transactions_from_file('2', test_filename)
    assert result2 is None

    result3 = get_transactions_from_file('3', test_filename)
    assert result3 is None


def test_get_transactions_from_file_wrong_key():

    result = get_transactions_from_file('4', 'test.path')
    assert result is None


def test_get_file_by_drag_and_drop_file_not_found(capsys):

    with (patch('src.get_transactions.sys.argv', ['script.py', 'missing.file']),
          patch('src.get_transactions.os.path.exists') as mock_path):

        mock_path.return_value = False

        result = get_file_by_drag_and_drop()

        assert result is None

        captured = capsys.readouterr()
        assert "Файл не найден: missing.file" in captured.out
