import json
import re


from typing import List, Dict, Any, Union


def check_filename(filename:str) -> Union[str,Exception]:
    if filename:
        wrong_chars = r'[<>:"/\\|?*\x00-\x1F]'
        if re.search(wrong_chars, filename):
            raise ValueError(f"Недопустимые символы в имени файла: {filename}")

    if len(filename) > 255:
        raise ValueError(f"Слишком длинное имя файла: {filename}")

    return filename


def open_json_transaction(filename: str) -> List[Dict[str, Any]]:
    transaction_json = check_filename(filename)
    try:
        with open(filename) as data_file:
            data = json.load(data_file)
            return data
    except json.JSONDecodeError as err:
        return f'Ошибка JSON^ {err}'
    except Exception as err:
        return f'Ошибка: {err}'
