from typing import Any, Dict, List, Iterator


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Iterator[Dict[str, Any]]:
    if transactions:
        for item in transactions:
            if item['operationAmount']['currency']['code'] == currency:
                yield item
    else:
        yield ''


def transaction_descriptions(transaction: List[Dict[str, Any]]) -> Iterator[Any]:
    if transaction:
        for item in transaction:
            yield item.get('description')
    else:
        yield ''


def card_number_generator(start: int, end: int) -> Iterator[str]:
    if start >= 1 and end < 9999999999999999 and end >= start:
        mask = 10000000000000000
        for num in range(start, end + 1):
            value = str(mask + num)
            card_number = f'{value[1:5]} {value[5:9]} {value[9:13]} {value[13:]}'
            yield card_number
    else:
        yield ''
