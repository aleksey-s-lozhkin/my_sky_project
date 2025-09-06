import json
import re
from typing import Any, Dict, List, Union

from src.external_api import currency_convert


def check_json_filename(filename: str) -> str:
    """Вспомогательная функция для проверки корректного ввода JSON файла с данными о транзакциях"""

    if filename:
        wrong_chars = r'[<>:"\\|?*\x00-\x1F]'
        if re.search(wrong_chars, filename):
            raise ValueError(f"Недопустимые символы в имени файла: {filename}")

    if len(filename) > 255:
        raise ValueError(f"Слишком длинное имя файла: {filename}")

    return filename


def open_json_transactions(json_path: str) -> Union[List[Dict[str, Any]], str]:
    """Функция принимает на вход путь до JSON - файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список."""

    filename = check_json_filename(json_path)
    try:
        with open(filename, 'r', encoding='utf-8') as data_file:
            data_list = list(json.load(data_file))
            if len(data_list) == 0:
                return ''
            return data_list
    except json.JSONDecodeError:
        return ''
    except FileNotFoundError:
        return ''
    except PermissionError:
        return ''
    except UnicodeDecodeError:
        return ''


def amount_transactions(transaction: Dict[str, Any], additional_amount: str) -> float:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float. Если
    транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют и конвертации
    суммы операции в рубли. Для конвертации используется Exchange Rates Data API"""

    operation_amount = transaction.get('operationAmount', {})
    if operation_amount == {}:
        raise KeyError('Key "operationAmount" is missing')
    currency = operation_amount.get('currency', {})
    if currency == {}:
        raise KeyError('Key "currency" is missing')
    value = operation_amount.get('amount', '')
    if value == '':
        raise KeyError('Key "amount" is missing')
    code = currency.get('code', '')
    if code == '':
        raise KeyError('Key "code" is missing')

    transaction_value = float(value)
    additional_value = float(additional_amount)

    if code in ['USD', 'EUR']:
        converted_amount = currency_convert(code, value)
        return converted_amount + additional_value
    elif code == 'RUB':
        return transaction_value + additional_value
    else:
        raise ValueError('Currency must be "RUB", "USD" or "EUR"')
