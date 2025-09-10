from typing import Any, Dict, List

import pandas as pd


def read_transactions_from_csv(file_path: str) -> List[Dict[Any, Any]]:
    """Функция читает финансовые операции из CSV-файла. Параметры: file_path (str) - путь к CSV-файлу. Возвращает:
    list - список словарей с операциями"""

    try:
        df = pd.read_csv(file_path, delimiter=';')
        return df.to_dict('records')

    except FileNotFoundError:
        raise FileNotFoundError(f"CSV file not found: {file_path}")

    except Exception as e:
        raise ValueError(f"Error while reading CSV file: {e}")


def read_transactions_from_excel(file_path: str, sheet_name: int | str = 0) -> List[Dict[Any, Any]]:
    """Функция читает финансовые операции из Excel-файла. Параметры: file_path (str)- путь к Excel-файлу
    sheet_name (str/int) - название или индекс листа. Возвращает: list - список словарей с операциями"""

    try:
        df = pd.read_excel(file_path, sheet_name)
        return df.to_dict('records')

    except FileNotFoundError:
        raise FileNotFoundError(f"Excel file not found: {file_path}")

    except Exception as e:
        raise ValueError(f"Error while reading excel file: {e}")
