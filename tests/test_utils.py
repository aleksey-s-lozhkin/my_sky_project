import os
import pytest

from unittest.mock import patch

from src.utils import amount_transactions, open_json_transactions


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
    assert open_json_transactions('test_empty.json') == ''


def test_nonexist_file_json():
    assert open_json_transactions('nonexist.json') == ''


def test_invalid_json():
    assert open_json_transactions('test_wrong.json') == ''


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
    wrong_names = [
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

    for wrong_dict, expected_error in wrong_names:
        with pytest.raises(KeyError, match=expected_error):
            amount_transactions(wrong_dict, '10000')
