import json
from collections import Counter

from mypy.types import names

from src.transaction_analyzer import process_bank_search
from src.utils import open_json_transactions
from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel


def main():
    print(
        'Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n'
        '1. Получить информацию о транзакциях из JSON-файла\n'
        '2. Получить информацию о транзакциях из CSV-файла\n'
        '3. Получить информацию о транзакциях из XLSX-файла'
    )

    read_from = 0

    while read_from not in ['1', '2', '3', '0']:
        read_from = input('Выберите необходимый пункт меню (0 - для выхода): ')

    if read_from == '1':
        print('Для обработки выбран JSON-файл')
        json_path = input('Введите путь к JSON файлу: ')
        try:
            list_transaction = open_json_transactions(json_path)
        except json.JSONDecodeError:
            print(f'Error decoding JSON in the file: {json_path}')
            return None

        except FileNotFoundError:
            print(f'File not found: {json_path}')
            return None

        except PermissionError:
            print(f'No access rights to the file: {json_path}')
            return None

        except UnicodeDecodeError:
            print(f'File decoding error: {json_path}')
            return None

        except ValueError as err:
            print(f'Error in the file name: {err}')
            return None

    elif read_from == '2':
        print('Для обработки выбран CSV-файл')
        csv_path = input('Введите путь к CSV файлу:' )
        try:
            list_transaction = read_transactions_from_csv(csv_path)
        except FileNotFoundError as e:
            print(f"CSV file not found: {csv_path}. Code error^ {e}")
            return None

        except Exception as e:
            print(f"Error while reading CSV file: {e}")
            return None

    elif read_from == '3':
        print('Для обработки выбран XLSX-файл')
        xlsx_path = input('Введите путь к CSV файлу: ')
        try:
            list_transaction = read_transactions_from_excel(xlsx_path)

        except FileNotFoundError as e:
            print(f"Excel file not found: {xlsx_path}. Code error: {e}")
            return None

        except Exception as e:
            print(f"Error while reading excel file: {e}")
            return None

    else:
        return None

    description_counter = Counter(item['description'] for item in list_transaction)
    unic_description = list(description_counter.keys())
    unic_description_lower = [item.lower() for item in unic_description]

    print(f'Доступные для фильтровки статусы:{", ".join(unic_description):}')

    filter_str = ''

    while True:
        filter_str = input(f'Введите статус, по которому необходимо выполнить фильтрацию (или NO - для выхода из '
                           f'программы\n Доступные для фильтровки статусы: {unic_description}): ').strip().lower()

        if filter_str == 'no':
            print("Выход из программы...")
            break

        if filter_str in unic_description_lower:
            original_status = unic_description[unic_description_lower.index(filter_str)]
            print(f"Фильтруем по статусу: {original_status}")
            # выполнить фильтрацию
            break
        else:
            print(f'Статус операции "{filter_str}" недоступен')
            print(f'Доступные статусы: {", ".join(unic_description)}')

    sorted_list = process_bank_search(list_transaction,filter_str)

    date_status = input('Отсортировать операции по дате? Да/Нет': )

    # тут надо начинать с обработки ввода тупого пользователя!!!




