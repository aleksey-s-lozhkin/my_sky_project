from unittest.mock import patch

import pytest

from src.transaction_analyzer import process_bank_classification, process_bank_search, search_pattern_creator


def test_process_bank_search_error():
    with pytest.raises(ValueError, match='Data cannot be empty'):
        process_bank_search('', 'test')

    with pytest.raises(ValueError, match='Search query cannot be empty'):
        process_bank_search([{}], '')


def test_process_bank_classification_error():
    with pytest.raises(ValueError, match='Data cannot be empty'):
        process_bank_classification('', [])

    with pytest.raises(ValueError, match='Classification query cannot be empty'):
        process_bank_classification([{}], '')


@pytest.mark.parametrize(
    'value, expected',
    [
        ('перевод открытие', 'перевод|открытие'),
        ('перевод, открытие', 'перевод|открытие'),
        ('', ''),
        ('test1, test2', 'test1|test2'),
    ],
)
def test_search_pattern_creator(value, expected):
    assert search_pattern_creator(value) == expected


@patch('src.transaction_analyzer.search_pattern_creator')
def test_process_bank_search_sorted_by_description(mock_creator):
    data = [{'description': 'Перевод'}]
    mock_creator.return_value = 'Перевод'
    result = process_bank_search(data, 'Перевод')
    assert len(result) == 1
    mock_creator.assert_called_with('Перевод')


def test_process_bank_classification_sorted_by_description():
    data = [{'description': 'Перевод'}]
    classification = ['Перевод']
    assert process_bank_classification(data, classification) == {'Перевод': 1}
