import os
from cgitb import reset
from unittest.mock import Mock, patch

import pandas as pd
import pytest
import requests
from requests import ConnectionError, RequestException, Timeout

from src.transaction_reader import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


def test_read_empty_csv():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(cur_dir, 'test_empty_csv.csv')
    assert read_transactions_from_csv(csv_path) == []


@patch('src.transaction_reader.pd.read_csv')
def test_csv_file_not_found_error(mock_read_csv):
    mock_read_csv.side_effect = FileNotFoundError('CSV file not found')
    with pytest.raises(FileNotFoundError, match='CSV file not found'):
        read_transactions_from_csv('test_path')


@patch('src.transaction_reader.pd.read_csv')
def test_csv_value_error(mock_read_csv):
    mock_read_csv.side_effect = ValueError('Error while reading CSV file')
    with pytest.raises(ValueError, match='Error while reading CSV file'):
        read_transactions_from_csv('test_path')


@patch('src.transaction_reader.pd.read_excel')
def test_excel_file_not_found_error(mock_read_excel):
    mock_read_excel.side_effect = FileNotFoundError('Excel file not found')
    with pytest.raises(FileNotFoundError, match='Excel file not found'):
        read_transactions_from_excel('test_path')


@patch('src.transaction_reader.pd.read_excel')
def test_excel_value_error(mock_read_excel):
    mock_read_excel.side_effect = ValueError('Error while reading excel file')
    with pytest.raises(ValueError, match='Error while reading excel file'):
        read_transactions_from_excel('test_path')


@patch('src.transaction_reader.pd.read_excel')
def test_read_excel_success(mock_read_excel):
    test_data = [
        {
            'id': 2177828.0,
            'state': 'EXECUTED',
            'date': '2022-04-14T15:14:21Z',
            'amount': 24853.0,
            'currency_name': 'Yuan Renminbi',
            'currency_code': 'CNY',
            'from': 'Счет 38577962752140632721',
            'to': 'Счет 47657753885349826314',
            'description': 'Перевод со счета на счет',
        },
        {
            'id': 4699552.0,
            'state': 'EXECUTED',
            'date': '2022-03-23T08:29:37Z',
            'amount': 23423.0,
            'currency_name': 'Peso',
            'currency_code': 'PHP',
            'from': 'Discover 7269000803370165',
            'to': 'American Express 1963030970727681',
            'description': 'Перевод с карты на карту',
        },
    ]
    mock_df = pd.DataFrame(test_data)
    mock_read_excel.return_value = mock_df
    result = read_transactions_from_excel('test_path')
    assert result == test_data


@patch('src.transaction_reader.pd.read_csv')
def test_read_csv_success(mock_read_csv):
    test_data = [
        {
            'id': 2177828.0,
            'state': 'EXECUTED',
            'date': '2022-04-14T15:14:21Z',
            'amount': 24853.0,
            'currency_name': 'Yuan Renminbi',
            'currency_code': 'CNY',
            'from': 'Счет 38577962752140632721',
            'to': 'Счет 47657753885349826314',
            'description': 'Перевод со счета на счет',
        },
        {
            'id': 4699552.0,
            'state': 'EXECUTED',
            'date': '2022-03-23T08:29:37Z',
            'amount': 23423.0,
            'currency_name': 'Peso',
            'currency_code': 'PHP',
            'from': 'Discover 7269000803370165',
            'to': 'American Express 1963030970727681',
            'description': 'Перевод с карты на карту',
        },
    ]
    mock_df = pd.DataFrame(test_data)
    mock_read_csv.return_value = mock_df
    result = read_transactions_from_csv('test_path')
    assert result == test_data
