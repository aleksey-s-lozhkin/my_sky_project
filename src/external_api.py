import os
from typing import Union

import requests
from dotenv import load_dotenv
from requests.exceptions import ConnectionError, HTTPError, RequestException, Timeout


def currency_convert(currency: str, amount: Union[float, int]) -> float:
    """Функция конвертирует сумму из указанной валюты в рубли используя Exchange Rates Data API. Аргументы:
    currency: Код валюты (например, 'USD', 'EUR') (str), amount: Сумма для конвертации (float или integer).
    Возвращает: Результат конвертации в рублях (float) или сообщение об ошибке если что-то пошло не так (str)"""

    load_dotenv()

    apilayer_api_key = os.getenv('API_KEY')
    if not apilayer_api_key:
        raise ValueError('API_KEY not found')

    if currency not in ['USD', 'EUR']:
        raise ValueError('Currency must be "USD" or "EUR"')

    try:
        if amount <= 0:
            raise ValueError('Amount must be more than zero')
    except TypeError:
        raise TypeError('Amount must be float or integer')

    headers = {"apikey": apilayer_api_key}
    url = f'https://api.apilayer.com/exchangerates_data/convert?to=RUB&from={currency}&amount={str(amount)}'

    try:
        response = requests.request("GET", url, headers=headers)
        if response.status_code != 200:
            raise HTTPError(f'HTTP Error {response.status_code}')
        get_convert = response.json()
        return float(get_convert['result'])

    except Timeout:
        raise Timeout('Error. Timeout')

    except ConnectionError:
        raise ConnectionError('Error. Check internet connection')

    except RequestException as err:
        raise RequestException(f'Error: {str(err)}')

    except (KeyError, ValueError) as err:
        raise ValueError(f'Incorrect data format: {str(err)}')
