from typing import Any, Dict

from src.widget import get_date, mask_account_card


def output_handler_json(transaction: Dict[str, Any]) -> list[Any]:
    """Вспомогательная функция для обработки вывода при работе с json"""

    result = []

    raw_date = transaction.get('date', 'unknown')
    if raw_date != 'unknown':
        result.append(get_date(raw_date))
    else:
        result.append(raw_date)

    result.append(transaction.get('description', 'unknown'))

    from_value = transaction.get('from', '')
    to_value = transaction.get('to', 'unknown')
    if not from_value == '':
        result.append(f'{mask_account_card(from_value)} -> {mask_account_card(to_value)}')
    else:
        result.append(f'{mask_account_card(to_value)}')

    operation_amount_value = transaction.get(
        'operationAmount', {'amount': '', 'currency': {'name': 'unknown', 'code': 'unknown'}}
    )
    result.append(operation_amount_value.get('amount', 'unknown'))
    currency_value = operation_amount_value.get('currency', {'name': 'unknown', 'code': 'unknown'})
    result.append(currency_value.get('name', 'unknown'))

    return result


def output_handler_xlsx_csv(transaction: Dict[str, Any]) -> list[Any]:
    """Вспомогательная функция для обработки вывода при работе xlsx, csv"""

    result = []

    raw_date = transaction.get('date', 'unknown')
    if raw_date != 'unknown':
        result.append(get_date(raw_date))
    else:
        result.append(raw_date)

    result.append(transaction.get('description', 'unknown'))

    from_value = transaction.get('from')
    to_value = transaction.get('to', 'unknown')

    if not from_value != from_value:
        result.append(f'{mask_account_card(from_value)} -> {mask_account_card(to_value)}')
    else:
        result.append(f'{mask_account_card(to_value)}')

    result.append(transaction.get('amount', 'unknown'))
    result.append(transaction.get('currency_name', 'unknown'))

    return result
