import json
import os
import sys
from typing import Any, Dict, List

from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel
from src.utils import open_json_transactions


def get_file_by_drag_and_drop():
    """Получает путь к файлу через перетаскивание в консоль"""

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        if os.path.exists(file_path):
            return file_path
        else:
            print(f"Файл не найден: {file_path}")
            return None

    print("Перетащите файл в окно терминала и нажмите Enter")
    file_path = input("Или введите путь к файлу: ").strip().strip('"')

    if os.path.exists(file_path):
        return file_path
    else:
        print(f"Файл не найден: {file_path}")
        return None


def get_transactions_from_file(read_from: str, source_file_name: str) -> List[Dict[str, Any]] | None:
    """Функция читает транзакции из файла в зависимости от выбранного формата '1' - JSON, '2' - CSV, '3' - XLSX.
    Возвращает: Список транзакций или None в случае ошибки"""

    if read_from == '1':
        json_path = source_file_name
        try:
            return list(open_json_transactions(json_path))
        except json.JSONDecodeError:
            print(f'Error decoding JSON in the file: {json_path}')
        except FileNotFoundError:
            print(f'File not found: {json_path}')
        except PermissionError:
            print(f'No access rights to the file: {json_path}')
        except UnicodeDecodeError:
            print(f'File decoding error: {json_path}')
        except ValueError as err:
            print(f'Error in the file name: {err}')
        return None

    elif read_from == '2':
        csv_path = source_file_name
        try:
            return read_transactions_from_csv(csv_path)
        except FileNotFoundError as e:
            print(f"CSV file not found: {csv_path}. Code error: {e}")
        except Exception as e:
            print(f"Error while reading CSV file: {e}")
        return None

    elif read_from == '3':
        xlsx_path = source_file_name
        try:
            return read_transactions_from_excel(xlsx_path)
        except FileNotFoundError as e:
            print(f"Excel file not found: {xlsx_path}. Code error: {e}")
        except Exception as e:
            print(f"Error while reading excel file: {e}")
        return None

    else:
        return None
