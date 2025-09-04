import json
from typing import Any, Dict, List, Union

from src.decorators import check_filename
from src.external_api import currency_convert


def open_json_transactions(filename: str) -> Union[List[Dict[str, Any]], str]:
    """Функция принимает на вход путь до JSON - файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список."""

    transaction_json = check_filename(filename)
    try:
        with open(transaction_json, 'r', encoding='utf-8') as data_file:
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
    except UnicodeDecodeError as err:
        return ''


def amount_transactions(transaction: Dict[str, Any], amount: float) -> float:
    """ Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float. Если
    транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют и конвертации
    суммы операции в рубли. Для конвертации используется Exchange Rates Data API"""

    code = transaction.get('operationAmount').get('currency').get('code')
    value = transaction.get('operationAmount').get('amount')
    result = 0
    if code == 'USD' or code == 'EUR':
        result = currency_convert(code, value) + amount
        return result
    else:
        result = amount + value
        return result
