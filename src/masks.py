import logging
import os
from functools import wraps
from typing import Any


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

    log_file_name = os.path.join(log_dir, 'masks.log')
    file_handler = logging.FileHandler(log_file_name, mode='w', encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formater)

    logger = logging.getLogger('mask_loger')
    logger.setLevel(logging.DEBUG)

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
def get_mask_card_number(card_number: str | Any) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован и отображается в формате
    XXXX XX** **** XXXX, где X — это цифра номера."""

    if len(card_number) == 0:
        logger.warning('Передан пустой номер карты')
        return ''

    if not card_number.isdigit():
        logger.error('Передан номер карты, содержащий символы')
        return ''

    if len(card_number) != 16:
        logger.error('Количество символов не соответствует длине номера карты')
        return ''

    result = f'{card_number[0:4]} {card_number[4:6]}** **** {card_number[12:]}'
    logger.info(f'Сгенерирована маска: {result}')

    return result


@log_function_call
def get_mask_account(account_number: str | Any) -> str:
    """Функция принимает на вход номер счета и возвращает его маску. Номер счета замаскирован и отображается в формате
    **XXXX, где X — это цифра номера."""

    if len(account_number) == 0:
        logger.warning('Передан пустой номер карты')
        return ''

    if not account_number.isdigit():
        logger.error('Передан номер карты, содержащий символы')
        return ''

    if len(account_number) != 20:
        logger.error('Количество символов не соответствует длине номера карты')
        return ''

    result = f'**{account_number[len(account_number) - 4:]}'
    logger.info(f'Сгенерирована маска: {result}')

    return result
