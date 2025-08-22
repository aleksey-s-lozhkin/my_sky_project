from typing import Any, Dict, Iterator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    """Функция принимает на вход список словарей, представляющих транзакции и возвращает итератор, который поочередно
    выдает транзакции, где валюта операции соответствует заданной (например, USD)"""

    if transactions:
        for item in transactions:
            if item['operationAmount']['currency']['code'] == currency:
                yield item
    else:
        yield {}


def transaction_descriptions(transaction: List[Dict[str, Any]]) -> Iterator[Any]:
    """Функция принимает список словарей с транзакциями и возвращает описание каждой операции по очереди"""

    if transaction:
        for item in transaction:
            yield item.get('description')
    else:
        yield ''


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """Функция выдает номера банковских карт в формате XXXX XXXX XXXX XXXX, где X — цифра номера карты. Генератор
    может сгенерировать номера карт в заданном диапазоне от 0000 0000 0000 0001 до 9999 9999 9999 9999"""

    if start >= 1 and end < 9999999999999999 and end >= start:
        mask = 10000000000000000
        for num in range(start, end + 1):
            value = str(mask + num)
            card_number = f'{value[1:5]} {value[5:9]} {value[9:13]} {value[13:]}'
            yield card_number
    else:
        yield ''
