import pytest

from src.widget import get_date, mask_account_card


def test_number_str_empty():
    assert mask_account_card('') == ''


def test_valid_bank_type():
    assert mask_account_card('Мир 7000792289606361') == ''


@pytest.mark.parametrize(
    'value, expected',
    [
        ('Maestro 1596837868705199', 'Maestro 1596 83** **** 5199'),
        ('Счет 64686473678894779589', 'Счет **9589'),
        ('MasterCard 7158300734726758', 'MasterCard 7158 30** **** 6758'),
        ('Visa Classic 6831982476737658', 'Visa Classic 6831 98** **** 7658'),
        ('Visa Platinum 8990922113665229', 'Visa Platinum 8990 92** **** 5229'),
        ('Visa Gold 5999414228426353', 'Visa Gold 5999 41** **** 6353'),
    ],
)
def test_card_valid(value, expected):
    assert mask_account_card(value) == expected


def test_valid_long():
    assert mask_account_card('Maestro 159683786870519') == ''
    assert mask_account_card('Maestro 15968378687051999') == ''


def test_date_str_empty():
    assert get_date('') == ''


def test_date_str_value():
    assert get_date('2024-03-11') == '11.03.2024'
    assert get_date('11-03-2024') == ''
    assert get_date('11/03/2024') == ''
    assert get_date('11/03/2024') == ''
    assert get_date('2024-03-11T02:26:18.671407') == '11.03.2024'
    assert get_date('2024-03-11 02:26:18') == '11.03.2024'
