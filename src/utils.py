import json
import logging
import os
import re
from functools import wraps
from typing import Any, Dict, List

from src.external_api import currency_convert


def setup_module_logger():
    """Функция для настройки логгера модуля. Формат записи лога в файл включает метку времени, название модуля, уровень
    серьезности и сообщение, описывающее событие или ошибку, которые произошли."""

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(cur_dir)
    log_dir = os.path.join(project_dir, 'logs')

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    formater = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
    )

    log_file_name = os.path.join(log_dir, 'utils.log')
    file_handler = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formater)

    logger = logging.getLogger('json_loger')
    logger.setLevel(logging.INFO)

    if logger.handlers:
        logger.handlers.clear()

    logger.addHandler(file_handler)

    return logger


logger = setup_module_logger()


def log_function_call(func):
    """Декоратор для логирования вызовов функций"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        function_name = func.__name__
        logger.info(
            f'Вызов функции {function_name} с позиционными аргументами: {args}, именованными аргументами: {kwargs}'
        )
        return func(*args, **kwargs)

    return wrapper


@log_function_call
def check_json_filename(filename: str) -> str:
    """Вспомогательная функция для проверки корректного ввода JSON файла с данными о транзакциях"""

    if filename:
        wrong_chars = r'[<>:"\\|?*\x00-\x1F]'
        if re.search(wrong_chars, filename):
            logger.error(f'Недопустимые символы в имени файла {filename}')
            raise ValueError(f"Недопустимые символы в имени файла: {filename}")

    if len(filename) > 255:
        logger.error(f'Слишком длинное имя файла {filename}')
        raise ValueError(f"Слишком длинное имя файла: {filename}")

    return filename


@log_function_call
def open_json_transactions(json_path: str) -> List[Dict[str, Any]]:
    """Функция принимает на вход путь до JSON - файла и возвращает список словарей с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден, функция возвращает пустой список."""

    filename = check_json_filename(json_path)
    logger.debug(f'Обработанное имя файла: {filename}')

    try:
        with open(filename, 'r', encoding='utf-8') as data_file:
            data_list = list(json.load(data_file))
            if len(data_list) == 0:

                logger.warning(f'Файл {filename} пустой')

                raise ValueError(f'Файл {filename} пустой')

            logger.info(f'Успешно загружено {len(data_list)} транзакций из файла {filename}')

            return data_list
    except json.JSONDecodeError:
        logger.error(f'Ошибка декодирования JSON в файле {filename}')
        raise

    except FileNotFoundError:
        logger.error(f'Файл не найден: {filename}')
        raise

    except PermissionError:
        logger.error(f'Нет прав доступа к файлу: {filename}')
        raise

    except UnicodeDecodeError:
        logger.error(f'Ошибка декодирования файла {filename}')
        raise


@log_function_call
def amount_transactions(transaction: Dict[str, Any], additional_amount: str) -> float:
    """Функция принимает на вход транзакцию и возвращает сумму транзакции (amount) в рублях, тип данных — float. Если
    транзакция была в USD или EUR, происходит обращение к внешнему API для получения текущего курса валют и конвертации
    суммы операции в рубли. Для конвертации используется Exchange Rates Data API"""

    operation_amount = transaction.get('operationAmount', {})

    if operation_amount == {}:
        logger.error('Отсутствует ключ "operationAmount"')
        raise KeyError('Key "operationAmount" is missing')

    currency = operation_amount.get('currency', {})

    if currency == {}:
        logger.error('Отсутствует ключ "currency"')
        raise KeyError('Key "currency" is missing')

    value = operation_amount.get('amount', '')

    if value == '':
        logger.error('Отсутствует ключ "amount"')
        raise KeyError('Key "amount" is missing')

    code = currency.get('code', '')

    if code == '':
        logger.error('Отсутствует ключ "code"')
        raise KeyError('Key "code" is missing')

    transaction_value = float(value)
    additional_value = float(additional_amount)

    if code in ['USD', 'EUR']:
        logger.info(f'Конвертация валюты {code} в RUB')
        converted_amount = currency_convert(code, value)
        result = converted_amount + additional_value
        logger.info(f'Итоговая сумма: {result} RUB (базовая: {transaction_value} + доп: {additional_value})')
        return result

    elif code == 'RUB':
        logger.info('Валюта в рублях, конвертация не требуется')
        result = transaction_value + additional_value
        logger.debug(f'Итоговая сумма: {result} RUB (базовая: {transaction_value} + доп: {additional_value})')
        return result

    else:
        logger.error(f'Неподдерживаемая валюта: "{code}". Допустимые значения: "RUB", "USD", "EUR"')
        raise ValueError('Currency must be "RUB", "USD" or "EUR"')
