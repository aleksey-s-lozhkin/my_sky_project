import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions
from tests.conftest import sample, transactions_empty, transactions_sample


def test_filter_sample(transactions_sample):
    gen = filter_by_currency(transactions_sample, 'USD')
    assert list(gen) == [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
    ]


def test_filter_empty(transactions_empty):
    gen = filter_by_currency(transactions_empty, 'USD')
    assert list(gen) == [{}]


def test_filter_sample(transactions_sample):
    gen = filter_by_currency(transactions_sample, 'EUR')
    assert list(gen) == []


def test_filter_sample(transactions_sample1):
    gen = filter_by_currency(transactions_sample1, 'EUR')
    assert list(gen) == [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]


def test_filter_sample(transactions_sample):
    gen = filter_by_currency(transactions_sample, 'RUB')
    assert list(gen) == [
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]


def test_card_extreme():
    gen = card_number_generator(5, 1)
    assert list(gen) == ['']
    gen = card_number_generator(9999999999999999, 10000000000000000)
    assert list(gen) == ['']
    gen = card_number_generator(-1, 5)
    assert list(gen) == ['']
    gen = card_number_generator(1, 10000000000000000)
    assert list(gen) == ['']
    gen = card_number_generator(5, 5)
    assert list(gen) == ['0000 0000 0000 0005']


def test_description_sample(transactions_sample):
    gen = transaction_descriptions(transactions_sample)
    assert list(gen) == [
        'Перевод организации',
        'Перевод со счета на счет',
        'Перевод со счета на счет',
        'Перевод с карты на карту',
        'Перевод организации',
    ]


def test_description_empty(transactions_empty):
    gen = transaction_descriptions(transactions_empty)
    assert list(gen) == ['']


def test_description_sample(transactions_sample1):
    gen = transaction_descriptions(transactions_sample1)
    assert list(gen) == ['Перевод организации']


@pytest.mark.parametrize(
    'val1, val2, expected',
    [
        (
            1,
            5,
            [
                '0000 0000 0000 0001',
                '0000 0000 0000 0002',
                '0000 0000 0000 0003',
                '0000 0000 0000 0004',
                '0000 0000 0000 0005',
            ],
        ),
        (
            11111,
            11115,
            [
                '0000 0000 0001 1111',
                '0000 0000 0001 1112',
                '0000 0000 0001 1113',
                '0000 0000 0001 1114',
                '0000 0000 0001 1115',
            ],
        ),
        (
            111111111,
            111111115,
            [
                '0000 0001 1111 1111',
                '0000 0001 1111 1112',
                '0000 0001 1111 1113',
                '0000 0001 1111 1114',
                '0000 0001 1111 1115',
            ],
        ),
        (
            1111111111111,
            1111111111115,
            [
                '0001 1111 1111 1111',
                '0001 1111 1111 1112',
                '0001 1111 1111 1113',
                '0001 1111 1111 1114',
                '0001 1111 1111 1115',
            ],
        ),
        (
            4321111111111111,
            4321111111111115,
            [
                '4321 1111 1111 1111',
                '4321 1111 1111 1112',
                '4321 1111 1111 1113',
                '4321 1111 1111 1114',
                '4321 1111 1111 1115',
            ],
        ),
    ],
)
def test_card_value(val1, val2, expected):
    gen = card_number_generator(val1, val2)
    assert list(gen) == expected
