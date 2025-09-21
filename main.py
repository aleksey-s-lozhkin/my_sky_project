from collections import Counter
from typing import Any, Dict, List

from src.processing import sort_by_date
from src.transaction_analyzer import (
    get_transactions_from_file,
    output_handler_json,
    output_handler_xlsx_csv,
    process_bank_search,
)

# from src.transaction_reader import read_transactions_from_csv, read_transactions_from_excel


def main() -> List[Dict[str, Any]] | None:
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

    read_from = ''

    while read_from not in ['1', '2', '3', '0']:
        read_from = input('Выберите необходимый пункт меню (0 - для выхода): ')
        if read_from not in ['1', '2', '3', '0']:
            print('Введите "1", "2", "3" или "0" - для выхода из программы')

    data_source = [
        'Выход из программы',
        'Для обработки выбран JSON-файл',
        'Для обработки выбран CSV-файл',
        'Для обработки выбран XLSX-файл',
    ]
    print(data_source[int(read_from)])
    source_file_name = input('Введите путь к файлу с транзакциями: ').strip().lower()

    list_transaction = get_transactions_from_file(read_from, source_file_name)
    if list_transaction is None:
        print('Нет транзакций для сортировки')
        return None

    # Выбор статуса интересующих операций
    state_counter = Counter(item.get('state', 'unknown') for item in list_transaction)
    unic_state = list(state_counter.keys())
    unic_state_lower = [item.lower() for item in unic_state]

    print(f'Доступные для фильтровки статусы:{", ".join(unic_state):}')

    while True:
        filter_str = (
            input(
                f'Введите статус, по которому необходимо выполнить фильтрацию \n'
                f' Доступные для фильтровки статусы: {', '.join(unic_state)}: '
            )
            .strip()
            .lower()
        )

        if filter_str in unic_state_lower:
            original_status = unic_state[unic_state_lower.index(filter_str)]
            print(f"Фильтруем по статусу: {original_status}")
            break
        else:
            print(f'Статус операции "{filter_str}" недоступен')
            print(f'Доступные статусы: {", ".join(unic_state)}')

    try:
        sorted_list = process_bank_search(list_transaction, filter_str)

    except ValueError as err:
        print(f'Ошибка: {err}')

    # Выбор статуса сортировки по дате
    while True:
        date_status = (
            input('Отсортировать операции по дате? Да/Нет: ').strip().lower()
        )

        if date_status == 'нет':
            print('Сортировка по дате не будет применена')
            break

        if date_status == 'да':

            while True:
                sorting_direction = (
                    input(
                        'Отсортировать операции по возрастанию или убыванию? '
                        'по возрастанию / по убыванию:  '
                    )
                    .strip()
                    .lower()
                )

                if sorting_direction in ['по возрастанию', 'по убыванию']:
                    direction = sorting_direction == 'по убыванию'
                    try:
                        sorted_list = sort_by_date(sorted_list, direction)
                    except KeyError:
                        print('Не все транзакции содержат дату. Сортировка не возможна.')
                        break
                    break

                else:
                    print('Выберите направление сортировки')
        else:
            print('Введите "да" или "нет"')

    # Выбор статуса вывода только рублевых операций

    while True:
        currency_status = (
            input('Выводить только рублевые операции? Да/Нет: ').strip().lower()
        )

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

        print('Введите "да" или "нет"')

    # Выбор статуса сортировки по определенному слову в описании

    while True:
        process_status = (
            input(
                'Отфильтровать список транзакций по определенному слову в описании? '
                'Да/Нет: '
            )
            .strip()
            .lower()
        )

        if process_status == 'нет':
            break

        if process_status == 'да':
            while True:
                description_counter = Counter(item.get('description', 'unknown') for item in list_transaction)
                unic_description = list(description_counter.keys())

                search_words = (
                    input(
                        f'Введите слово или фразу для поиска (quit - для выхода из программы, '
                        f'пустая строка - отмена фильтрации). Возможные варианты для фильтрации: '
                        f'{', '.join(unic_description)}: '
                    )
                    .strip()
                    .lower()
                )
                if search_words == '':
                    break

                sorted_list = process_bank_search(sorted_list, search_words)

            if search_words == '':
                print('Фильтрация по словам не будет применена')
                break

    # Вывод результатов работы программы

    if len(sorted_list) > 0:
        print('Вывожу итоговый список транзакций...')
        print(f'Всего банковских операций в выборке: {len(sorted_list)}')

        for transaction in sorted_list:

            if read_from in ['2', '3']:
                handler = output_handler_xlsx_csv(transaction)
            else:
                handler = output_handler_json(transaction)

            print(f'{handler[0]} {handler[1]}\n' f'{handler[2]}\n' f'Сумма: {handler[3]} {handler[4]}')
    else:
        print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации')

    return sorted_list
