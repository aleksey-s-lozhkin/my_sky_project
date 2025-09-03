import json

from src.external_api import currency_convert
from src.decorators import check_filename

from typing import List, Dict, Any, Union


def open_json_transactions(filename: str) -> Union[List[Dict[str, Any]], str]:
    transaction_json = check_filename(filename)
    try:
        with open(transaction_json, 'r', encoding='utf-8') as data_file:
            data_list = list(json.load(data_file))
            if len(data_list) == 0:
                return ''
            return data_list
    except json.JSONDecodeError:
        return ''
    except FileNotFoundError:
        return ''
    except PermissionError:
        return ''
    except UnicodeDecodeError as err:
        return ''


def amount_transactions(transaction: Dict[str, Any], amount: float) -> float:
    code = transaction.get('operationAmount').get('currency').get('code')
    value = transaction.get('operationAmount').get('amount')
    result = 0
    if code == 'USD' or code == 'EUR':
        result = currency_convert(code, value) + amount
        return result
    else:
        result = amount + value
        return result
