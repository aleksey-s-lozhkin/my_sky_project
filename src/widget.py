from datetime import datetime

from .masks import get_mask_account, get_mask_card_number


def mask_account_card(number_str: str) -> str:
    """Функция принимает на вход строку, содержащую тип и номер карты или счета и возвращает строку
    с замаскированным номером. Для карт и счетов используются разные типы маскировки"""

    if 'Счет' in number_str:
        return get_mask_account(number_str[-20:])
    else:
        return get_mask_card_number(number_str[-16:])


def get_date(date_str: str) -> str:
    """Функция принимает на вход строку с датой в формате '2024-03-11T02:26:18.671407'
    и возвращает строку с датой в формате 'ДД.ММ.ГГГГ'"""

    dt = datetime.fromisoformat(date_str)
    return dt.strftime('%d.%m.%Y')
