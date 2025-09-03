import requests
from dotenv import load_dotenv
import os
import json
from typing import Union

def currency_convert(currency: str, amount: float) -> Union[float, str]:


    load_dotenv()
    apilayer_api_key = os.getenv('API_KEY')

    if not apilayer_api_key:
        return "API_KEY not found"

    headers ={"apikey": apilayer_api_key}
    url = 'https://api.apilayer.com/exchangerates_data/convert'
    payload = {"amount": str(amount), "from": currency, "to": 'RUB'}

    response = requests.get(url, headers=headers, params=payload)
    status_code = response.status_code
    get_convert = response.json()

    return float(get_convert['result'])
