import json
import os
from typing import Union

import requests
from dotenv import load_dotenv


def currency_convert(currency: str, amount: Union[float, int]) -> Union[float, str]:
    """Функция конвертирует сумму из указанной валюты в рубли используя Exchange Rates Data API. Аргументы:
    currency: Код валюты (например, 'USD', 'EUR') (str), amount: Сумма для конвертации (float или integer).
    Возвращает: Результат конвертации в рублях (float) или сообщение об ошибке если что-то пошло не так (str)"""

    load_dotenv()

    apilayer_api_key = os.getenv('API_KEY')
    if not apilayer_api_key:
        return 'API_KEY not found'

    if currency not in ['USD', 'EUR']:
        return 'Currency must be "USD" or "EUR"'

    if amount <= 0:
        return 'Amount must be more than zero'

    headers = {"apikey": apilayer_api_key}
    url = f'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={str(amount)}'
    payload = {}

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        if response.status_code != 200:
            return f'HTTP Error {response.status_code}'
        get_convert = response.json()
        return float(get_convert['result'])
    except requests.exceptions.Timeout:
        return 'Error. Timeout'
    except requests.exceptions.RequestException as err:
        return f'Error: {str(err)}'
    except requests.exceptions.ConnectionError:
        return 'Error. Check internet connection'
