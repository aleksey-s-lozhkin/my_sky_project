import json
from collections import Counter

from typing import Any, Dict, List

from src.transaction_analyzer import process_bank_search
from src.utils import open_json_transactions
from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel
from src.processing import sort_by_date
from src.widget import get_date, mask_account_card


def output_handler(transaction: Dict[str, Any]) -> list[Any]:
    """Вспомогательная функция для обработки вывода"""

    result =[]

    raw_date = transaction.get('date', 'unknown')
    if raw_date != 'unknown':
        result.append(get_date(raw_date))
    else:
        result.append(raw_date)

    result.append(transaction.get('state', 'unknown'))

    from_value = transaction.get('from', '')
    to_value = transaction.get('to', 'unknown')
    if not from_value == '':
        result.append(f'{mask_account_card(from_value)} -> {mask_account_card(to_value)}')
    else:
        result.append(f'{mask_account_card(to_value)}')

    operation_amount_value = transaction.get('operationAmount', {'amount':'','currency': {'name':'unknown',
                                                                                          'code':'unknown'}})
    result.append(operation_amount_value.get('amount', 'unknown'))
    currency_value = operation_amount_value.get('currency', {'name':'unknown','code':'unknown'})
    result.append(currency_value.get('name', 'unknown'))

    return result



def main() -> List[Dict[str,Any]]|None:
    """Функция отвечает за основную логику проекта, взаимодействие с пользователем и связывает функциональности
    между собой."""

    sorted_list = []

    # Выбор откуда будем читать информацию о транзакциях
    print(
        'Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n'
        '1. Получить информацию о транзакциях из JSON-файла\n'
        '2. Получить информацию о транзакциях из CSV-файла\n'
        '3. Получить информацию о транзакциях из XLSX-файла'
    )

    read_from = 0

    while read_from not in ['1', '2', '3', '0']:
        read_from = input('Выберите необходимый пункт меню (0 - для выхода): ')
        if read_from not in ['1', '2', '3', '0']:
            print('Введите "1", "2", "3" или "0" - для выхода из программы')

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


    # Выбор статуса интересующих операций
    state_counter = Counter(item.get('state', 'unknown') for item in list_transaction)
    unic_state = list(state_counter.keys())
    unic_state_lower = [item.lower() for item in unic_state]

    print(f'Доступные для фильтровки статусы:{", ".join(unic_state):}')

    while True:
        filter_str = input(f'Введите статус, по которому необходимо выполнить фильтрацию (или quit - для выхода из '
                           f'программы)\n Доступные для фильтровки статусы: {', '.join(unic_state)}: '
                           f'').strip().lower()

        if filter_str == 'quit':
            print('Выход из программы...')
            return None

        if filter_str in unic_state_lower:
            original_status = unic_state[unic_state_lower.index(filter_str)]
            print(f"Фильтруем по статусу: {original_status}")
            break
        else:
            print(f'Статус операции "{filter_str}" недоступен')
            print(f'Доступные статусы: {", ".join(unic_state)}')

    try:
        sorted_list = process_bank_search(list_transaction,filter_str)

    except ValueError as err:
        print(f'Ошибка: {err}')

    # Выбор статуса сортировки по дате
    while True:
        date_status = (input('Отсортировать операции по дате? Да/Нет (quit - для выхода из программы): ')
                       .strip().lower())

        if date_status == 'quit':
            print('Выход из программы...')
            return None

        if date_status == 'нет':
            print('Сортировка по дате не будет применена')
            break

        if date_status == 'да':

            while True:
                sorting_direction = (input('Отсортировать операции по возрастанию или убыванию? '
                                          'по возрастанию / по убыванию (quit - для выхода из программы):  ')
                                     .strip().lower())

                if sorting_direction == 'quit':
                    print('Выход из программы...')
                    return None

                elif sorting_direction in ['по возрастанию', 'по убыванию']:
                    direction = sorting_direction == 'по убыванию'
                    try:
                        sorted_list = sort_by_date(sorted_list,direction)
                    except KeyError:
                        print('Не все транзакции содержат дату. Сортировка не возможна.')
                        break
                    break

                else:
                    print('Выберите направление сортировки')
        else:
            print('Введите "да", "нет" или "quit"')

    # Выбор статуса вывода только рублевых операций

    while True:
        currency_status = (input('Выводить только рублевые операции? Да/Нет (quit - для выхода из программы): ')
                           .strip().lower())

        if currency_status == 'quit':
            print('Выход из программы...')
            return None

        if currency_status == 'нет':
            print('Фильтр по рублевым операциям не будет применен')
            break

        if currency_status == 'да':
            try:
                sorted_list = [item for item in sorted_list if item['operationAmount']['currency']['code'] == 'RUB']
                break
            except KeyError:
                print('Не все транзакции содержат код валюты. Сортировка не возможна.')
                break

        print('Введите "да", "нет" или "quit"')

    # Выбор статуса сортировки по определенному слову в описании

    while True:
        process_status = input('Отфильтровать список транзакций по определенному слову в описании? '
                               'Да/Нет (quit - для выхода из программы): ').strip().lower()

        if process_status == 'quit':
            print('Выход из программы...')
            return None

        if process_status == 'нет':
            break

        if process_status == 'да':
            while True:
                description_counter = Counter(item.get('description', 'unknown') for item in list_transaction)
                unic_description = list(description_counter.keys())
                print('')
                search_words = input(f'Введите слово или фразу для поиска (quit - для выхода из программы, '
                                    f'пустая строка - отмена фильтрации). Возможные варианты для фильтрации: '
                                    f'{', '.join(unic_description)}: ').strip().lower()
                if search_words =='':
                    break

                if search_words == 'quit':
                    print('Выход из программы...')
                    return None

                sorted_list = process_bank_search(sorted_list, search_words)

            if search_words == '':
                print('Фильтрация по словам не будет применена')
                break

    # Вывод результатов работы программы

    print('Вывожу итоговый список транзакций...')
    print(f'Всего банковских операций в выборке: {len(sorted_list)}')
    for transaction in sorted_list:
        print(f'{output_handler(transaction)[0]} {output_handler(transaction)[1]}'
              f'\n{output_handler(transaction)[2]}'
              f'\nСумма: {output_handler(transaction)[3]} {output_handler(transaction)[4]}')

