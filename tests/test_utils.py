import os
import pytest

from unittest.mock import patch

from src.utils import amount_transactions, open_json_transactions


#Tests for open_json_transactions
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
    assert open_json_transactions(json_path) == ''


def test_nonexist_file_json():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'nonexist.json')
    assert open_json_transactions(json_path) == ''


def test_invalid_json():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(cur_dir, 'test_wrong.json')
    assert open_json_transactions(json_path) == ''


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


#Tests for amount_transactions
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
