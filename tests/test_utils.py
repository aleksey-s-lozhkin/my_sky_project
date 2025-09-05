import os

from unittest.mock import Mock

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
    assert amount_transactions()
