def get_mask_card_number(card_number: str) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску. Номер карты замаскирован и отображается в формате
    XXXX XX** **** XXXX, где X — это цифра номера."""

    if len(card_number) == 0:
        return ''

    if not card_number.isdigit():
        return ''

    if len(card_number) != 16:
        return ''

    return f'{card_number[0:4]} {card_number[4:6]}** **** {card_number[12:]}'


def get_mask_account(account_number: str) -> str:
    """Функция принимает на вход номер счета и возвращает его маску. Номер счета замаскирован и отображается в формате
    **XXXX, где X — это цифра номера."""

    if len(account_number) == 0:
        return ''

    if not account_number.isdigit():
        return ''

    if len(account_number) != 20:
        return ''

    return f'**{account_number[len(account_number) - 4:]}'
