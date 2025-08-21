import re
from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(number_str: str) -> str:
    """Функция принимает на вход строку, содержащую тип и номер карты или счета и возвращает строку
    с замаскированным номером. Для карт и счетов используются разные типы маскировки"""

    if len(number_str) == 0:
        return ''

    if re.match(r'Счет', number_str) and len(number_str) == 25:
        return f'Счет {get_mask_account(number_str[-20:])}'
    elif re.match(r'Visa Classic', number_str) and len(number_str) == 29:
        return f'Visa Classic {get_mask_card_number(number_str[-16:])}'
    elif re.match(r'Visa Gold', number_str) and len(number_str) == 26:
        return f'Visa Gold {get_mask_card_number(number_str[-16:])}'
    elif re.match(r'Visa Platinum', number_str) and len(number_str) == 30:
        return f'Visa Platinum {get_mask_card_number(number_str[-16:])}'
    elif re.match(r'Maestro', number_str) and len(number_str) == 24:
        return f'Maestro {get_mask_card_number(number_str[-16:])}'
    elif re.match(r'MasterCard', number_str) and len(number_str) == 27:
        return f'MasterCard {get_mask_card_number(number_str[-16:])}'
    else:
        return ''


def get_date(date_str: str) -> str:
    """Функция принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""

    if len(date_str) == 0:
        return ''

    try:
        dt = datetime.fromisoformat(date_str)
        return dt.strftime('%d.%m.%Y')
    except ValueError:
        return ''
