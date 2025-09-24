import math
from unittest.mock import patch

from src.output_handler import output_handler_json, output_handler_xlsx_csv


@patch('src.output_handler.mask_account_card')
@patch('src.output_handler.get_date')
def test_output_handler_json(mock_date, mock_mask):
    test_data1 = {
        'date': '100',
        'description': '200',
        'from': '300',
        'to': '400',
        'operationAmount': {'amount': '500', 'currency': {'name': '600'}},
    }
    test_data2 = {
        'date': '100',
        'description': '200',
        'from': '',
        'to': '400',
        'operationAmount': {'amount': '500', 'currency': {'name': '600'}},
    }
    test_data3 = {
        'date': 'unknown',
        'description': '200',
        'from': '',
        'to': '400',
        'operationAmount': {'amount': '500', 'currency': {'name': '600'}},
    }

    mock_mask.return_value = '222'
    mock_date.return_value = '111'

    result1 = output_handler_json(test_data1)
    assert result1 == ['111', '200', '222 -> 222', '500', '600']

    result2 = output_handler_json(test_data2)
    assert result2 == ['111', '200', '222', '500', '600']

    result3 = output_handler_json(test_data3)
    assert result3 == ['unknown', '200', '222', '500', '600']


@patch('src.output_handler.mask_account_card')
@patch('src.output_handler.get_date')
def test_output_handler_xlsx_csv(mock_date, mock_mask):
    test_data1 = {
        'date': '100',
        'description': '200',
        'from': 300,
        'to': 400,
        'amount': '500',
        'currency_name': '600',
    }
    test_data2 = {
        'date': '100',
        'description': '200',
        'from': math.nan,
        'to': 400,
        'amount': '500',
        'currency_name': '600',
    }
    test_data3 = {
        'date': 'unknown',
        'description': '200',
        'from': math.nan,
        'to': 400,
        'amount': '500',
        'currency_name': '600',
    }

    mock_mask.return_value = '222'
    mock_date.return_value = '111'

    result1 = output_handler_xlsx_csv(test_data1)
    assert result1 == ['111', '200', '222 -> 222', '500', '600']

    result2 = output_handler_xlsx_csv(test_data2)
    assert result2 == ['111', '200', '222', '500', '600']

    result3 = output_handler_xlsx_csv(test_data3)
    assert result3 == ['unknown', '200', '222', '500', '600']
