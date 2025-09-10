import os
from unittest.mock import patch

import pytest

from src.masks import get_mask_account, get_mask_card_number, setup_module_logger


def test_card_empty():
    assert get_mask_card_number('') == ''


def test_account_empty():
    assert get_mask_account('') == ''


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ('1596837868705199', '1596 83** **** 5199'),
        ('7158300734726758', '7158 30** **** 6758'),
        ('6831982476737658', '6831 98** **** 7658'),
        ('8990922113665229', '8990 92** **** 5229'),
        ('5999414228426353', '5999 41** **** 6353'),
    ],
)
def test_card_valid(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    'account_number, expected',
    [('64686473678894779589', '**9589'), ('35383033474447895560', '**5560'), ('73654108430135874305', '**4305')],
)
def test_account_valid(account_number, expected):
    assert get_mask_account(account_number) == expected


def test_card_isdigit():
    assert get_mask_card_number('1596 8378 6870 5199') == ''


def test_account_isdigit():
    assert get_mask_account('64686473678894779589 ') == ''


def test_card_amount_digit():
    assert get_mask_card_number('159683786870519') == ''


def test_account_amount_digit():
    assert get_mask_account('7365410843013587430') == ''


@patch('src.masks.os.path.exists')
@patch('src.masks.os.makedirs')
def test_create_log_dir(mock_makedirs, mock_exists):
    mock_exists.return_value = False

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(cur_dir)
    log_dir = os.path.join(project_dir, 'logs')
    setup_module_logger()

    mock_exists.assert_called_once_with(log_dir)
    mock_makedirs.assert_called_once_with(log_dir)


@patch('src.masks.os.path.exists')
@patch('src.masks.os.makedirs')
def test_not_create_log_dir(mock_makedirs, mock_exists):
    mock_exists.return_value = True

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(cur_dir)
    log_dir = os.path.join(project_dir, 'logs')
    setup_module_logger()

    mock_exists.assert_called_once_with(log_dir)
    mock_makedirs.assert_not_called()
