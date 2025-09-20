import re
from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(number_str: str) -> str:
    """Функция принимает на вход строку, содержащую тип и номер карты или счета и возвращает строку
    с замаскированным номером. Для карт и счетов используются разные типы маскировки"""

    if not number_str or not number_str.strip():
        return ''

    # Определяем тип карты/счета и извлекаем номер
    account_match = re.match(r'^Счет\s+(\d{20})$', number_str)
    if account_match:
        return f'Счет {get_mask_account(account_match.group(1))}'

    # Паттерны для карт с извлечением номера
    card_patterns = [
        (r'^Visa Classic\s+(\d{16})$', 'Visa Classic'),
        (r'^Visa Gold\s+(\d{16})$', 'Visa Gold'),
        (r'^Visa Platinum\s+(\d{16})$', 'Visa Platinum'),
        (r'^Maestro\s+(\d{16})$', 'Maestro'),
        (r'^MasterCard\s+(\d{16})$', 'MasterCard'),
    ]

    for pattern, card_type in card_patterns:
        match = re.match(pattern, number_str)
        if match:
            return f'{card_type} {get_mask_card_number(match.group(1))}'

    return ''


def get_date(date_str: str) -> str:
    """Функция принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""

    if not date_str or not date_str.strip():
        return ''

    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime('%d.%m.%Y')
    except (ValueError, AttributeError, TypeError):
        return ''
