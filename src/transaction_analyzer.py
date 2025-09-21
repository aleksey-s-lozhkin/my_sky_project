import json
import re
from collections import Counter
from typing import Any, Dict, List

from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel
from src.utils import open_json_transactions
from src.widget import get_date, mask_account_card


def search_pattern_creator(search: str) -> str:
    """Вспомогательная функция для подготовки поисковой строки"""

    words_list = re.findall(r'\w+', search)

    if not words_list:
        return ''

    return '|'.join(words_list)


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Функция для поиска в списке словарей операций по заданной строке возвращает список словарей с операциями, у
    которых в описании есть строка, переданная аргументу функции"""

    if not data:
        raise ValueError('Data cannot be empty')
    if not search:
        raise ValueError('Search query cannot be empty')

    pattern = re.compile(search_pattern_creator(search), re.IGNORECASE)
    sorted_by_description = [item for item in data if pattern.search(item.get('description', ''))]

    return sorted_by_description


def process_bank_classification(data: List[Dict[str, Any]], classification: List[str]) -> Dict[str, Any]:
    """Функция для подсчета количества банковских операций определенного типа возвращает словарь, в котором ключи —
    это названия категорий, а значения — это количество операций в каждой категории"""

    if not data:
        raise ValueError('Data cannot be empty')
    if not classification:
        raise ValueError('Classification query cannot be empty')

    sorted_by_description = [item for item in data if item.get('description') in classification]
    descriptions = [item['description'] for item in sorted_by_description]
    statistics_dict = Counter(descriptions)

    return dict(statistics_dict)


def get_transactions_from_file(read_from: str, source_file_name: str) -> List[Dict[str, Any]] | None:
    """Функция читает транзакции из файла в зависимости от выбранного формата '1' - JSON, '2' - CSV, '3' - XLSX.
    Возвращает: Список транзакций или None в случае ошибки"""

    if read_from == '1':
        json_path = source_file_name
        try:
            return open_json_transactions(json_path)
        except json.JSONDecodeError:
            print(f'Error decoding JSON in the file: {json_path}')
        except FileNotFoundError:
            print(f'File not found: {json_path}')
        except PermissionError:
            print(f'No access rights to the file: {json_path}')
        except UnicodeDecodeError:
            print(f'File decoding error: {json_path}')
        except ValueError as err:
            print(f'Error in the file name: {err}')
        return None

    elif read_from == '2':
        csv_path = source_file_name
        try:
            return read_transactions_from_csv(csv_path)
        except FileNotFoundError as e:
            print(f"CSV file not found: {csv_path}. Code error: {e}")
        except Exception as e:
            print(f"Error while reading CSV file: {e}")
        return None

    elif read_from == '3':
        xlsx_path = source_file_name
        try:
            return read_transactions_from_excel(xlsx_path)
        except FileNotFoundError as e:
            print(f"Excel file not found: {xlsx_path}. Code error: {e}")
        except Exception as e:
            print(f"Error while reading excel file: {e}")
        return None

    else:
        return None


def output_handler_json(transaction: Dict[str, Any]) -> list[Any]:
    """Вспомогательная функция для обработки вывода при работе с json"""

    result = []

    raw_date = transaction.get('date', 'unknown')
    if raw_date != 'unknown':
        result.append(get_date(raw_date))
    else:
        result.append(raw_date)

    result.append(transaction.get('state', 'unknown'))

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

    result.append(transaction.get('state', 'unknown'))

    from_value = transaction.get('from', '')
    to_value = transaction.get('to', 'unknown')
    if not from_value == '':
        result.append(f'{mask_account_card(from_value)} -> {mask_account_card(to_value)}')
    else:
        result.append(f'{mask_account_card(to_value)}')

    result.append(transaction.get('amount', 'unknown'))
    result.append(transaction.get('currency_name', 'unknown'))

    return result
