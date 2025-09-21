import pytest

from src.transaction_analyzer import process_bank_classification, process_bank_search, search_pattern_creator


def test_process_bank_search():
    with pytest.raises(ValueError, match='Data cannot be empty'):
        process_bank_search('', 'test')

    with pytest.raises(ValueError, match='Search query cannot be empty'):
        process_bank_search([{}], '')


def test_process_bank_classification():
    with pytest.raises(ValueError, match='Data cannot be empty'):
        process_bank_classification('', [])

    with pytest.raises(ValueError, match='Classification query cannot be empty'):
        process_bank_classification([{}], '')
