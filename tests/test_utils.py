import os

from json import JSONDecodeError
from unittest.mock import patch

import pytest

from src.utils import amount_transactions, open_json_transactions, setup_module_logger


# Tests for open_json_transactions
def test_valid_json():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'test.json')
    assert open_json_transactions(json_path) == [
        {
            'date': '2019-08-26T10:50:58.294041',
            'description': 'Перевод организации',
            'from': 'Maestro 1596837868705199',
            'id': 441945886,
            'operationAmount': {'amount': '20000', 'currency': {'code': 'RUB', 'name': 'руб.'}},
            'state': 'EXECUTED',
            'to': 'Счет 64686473678894779589',
        }
    ]


def test_empty_json():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'test_empty.json')
    with pytest.raises(JSONDecodeError, match='Expecting value'):
        open_json_transactions(json_path)


def test_nonexist_file_json():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'nonexist.json')
    with pytest.raises(FileNotFoundError, match='Файл не найден: nonexist.json'):
        open_json_transactions(json_path)


def test_invalid_json():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'test_wrong.json')
    with pytest.raises(JSONDecodeError, match='Ошибка декодирования JSON в файле test_wrong.json'):
        open_json_transactions(json_path)


def test_incorrect_json():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'test_incorrect.json')
    assert open_json_transactions(json_path) == ''


def test_wrong_json_filenames():
    wrong_names = [
        ('file<name.log', "Недопустимые символы"),
        ('file>name.log', "Недопустимые символы"),
        ('file:name.log', "Недопустимые символы"),
        ('file"name.log', "Недопустимые символы"),
        ('file\\name.log', "Недопустимые символы"),
        ('file|name.log', "Недопустимые символы"),
        ('file?name.log', "Недопустимые символы"),
        ('file*name.log', "Недопустимые символы"),
        ('a' * 256, "Слишком длинное имя"),
    ]

    for filename, expected_error in wrong_names:
        with pytest.raises(ValueError, match=expected_error):
            cur_dir = os.path.dirname(os.path.abspath(__file__))
            json_path = os.path.join(cur_dir, filename)
            open_json_transactions(json_path)


# Tests for amount_transactions
def test_rub_transaction():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'test.json')
    assert amount_transactions(open_json_transactions(json_path)[0], '10000') == 30000


def test_usd_transaction():
    test_dict = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "20000", "currency": {"name": "руб.", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }
    with patch('src.utils.currency_convert') as mock_currency_convert:
        mock_currency_convert.return_value = 30000.0
        res = amount_transactions(test_dict, 10000)
        assert res == 40000
        mock_currency_convert.assert_called_once_with('USD', '20000')


def test_eur_transaction():
    test_dict = {
        "id": 441945886,
        "state": "EXECUTED",
        "date": "2019-08-26T10:50:58.294041",
        "operationAmount": {"amount": "20000", "currency": {"name": "руб.", "code": "EUR"}},
        "description": "Перевод организации",
        "from": "Maestro 1596837868705199",
        "to": "Счет 64686473678894779589",
    }
    with patch('src.utils.currency_convert') as mock_currency_convert:
        mock_currency_convert.return_value = 30000.0
        res = amount_transactions(test_dict, 10000)
        assert res == 40000
        mock_currency_convert.assert_called_once_with('EUR', '20000')


def test_wrong_json():
    wrong_dicts = [
        (
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"currency": {"name": "руб.", "code": "EUR"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            },
            'Key "amount" is missing',
        ),
        (
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "20000", "currency": {"name": "руб."}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            },
            'Key "code" is missing',
        ),
        (
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "20000"},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            },
            'Key "currency" is missing',
        ),
        (
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            },
            'Key "operationAmount" is missing',
        ),
    ]

    for wrong_dict, expected_error in wrong_dicts:
        with pytest.raises(KeyError, match=expected_error):
            amount_transactions(wrong_dict, '10000')


def test_wrong_currency():
    wrong_dicts = [
        (
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "20000", "currency": {"name": "руб.", "code": "CNY"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            },
            'Currency must be "RUB", "USD" or "EUR"',
        ),
        (
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {"amount": "20000", "currency": {"name": "руб.", "code": "BYR"}},
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589",
            },
            'Currency must be "RUB", "USD" or "EUR"',
        ),
    ]

    for wrong_dict, expected_error in wrong_dicts:
        with pytest.raises(ValueError, match=expected_error):
            amount_transactions(wrong_dict, '10000')


@patch('src.utils.os.path.exists')
@patch('src.utils.os.makedirs')
def test_create_log_dir(mock_makedirs, mock_exists):
    mock_exists.return_value = False

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(cur_dir)
    log_dir = os.path.join(project_dir, 'logs')
    setup_module_logger()

    mock_exists.assert_called_once_with(log_dir)
    mock_makedirs.assert_called_once_with(log_dir)


@patch('src.utils.os.path.exists')
@patch('src.utils.os.makedirs')
def test_not_create_log_dir(mock_makedirs, mock_exists):
    mock_exists.return_value = True

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(cur_dir)
    log_dir = os.path.join(project_dir, 'logs')
    setup_module_logger()

    mock_exists.assert_called_once_with(log_dir)
    mock_makedirs.assert_not_called()


@patch('src.utils.check_json_filename')
@patch('src.utils.open')
@patch('src.utils.logger')
def test_open_json_transactions_permission_error(mock_logger, mock_open, mock_check_filename):
    test_filename = 'protected.json'
    mock_check_filename.return_value = test_filename
    mock_open.side_effect = PermissionError("Permission denied")
    result = open_json_transactions('protected.json')
    assert result == ''
    mock_check_filename.assert_called_once_with('protected.json')
    mock_open.assert_called_once_with(test_filename, 'r', encoding='utf-8')
    mock_logger.error.assert_called_once_with(f'Нет прав доступа к файлу: {test_filename}')


@patch('src.utils.check_json_filename')
@patch('src.utils.open')
@patch('src.utils.json.load')
@patch('src.utils.logger')
def test_open_json_transactions_empty_file(mock_logger, mock_json_load, mock_open, mock_check_filename):
    test_filename = 'test.json'
    mock_check_filename.return_value = test_filename
    mock_json_load.return_value = []

    result = open_json_transactions('test.json')
    assert result == ''
    mock_check_filename.assert_called_once_with('test.json')
    mock_open.assert_called_once_with(test_filename, 'r', encoding='utf-8')
    mock_logger.warning.assert_called_once_with(f'Файл {test_filename} пустой')
