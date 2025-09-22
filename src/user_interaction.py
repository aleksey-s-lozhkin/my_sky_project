from collections import Counter
from typing import Any, Dict, List

from output_handler import output_handler_json, output_handler_xlsx_csv
from processing import sort_by_date
from src.get_transactions import get_file_by_drag_and_drop, get_transactions_from_file
from transaction_analyzer import process_bank_search


def select_data_source() -> str:
    """Выбор источника данных"""

    print(
        'Привет! Добро пожаловать в программу работы с банковскими транзакциями.\n'
        '1. Получить информацию о транзакциях из JSON-файла\n'
        '2. Получить информацию о транзакциях из CSV-файла\n'
        '3. Получить информацию о транзакциях из XLSX-файла'
    )

    data_sources = {
        '0': 'Выход из программы',
        '1': 'Для обработки выбран JSON-файл',
        '2': 'Для обработки выбран CSV-файл',
        '3': 'Для обработки выбран XLSX-файл',
    }

    while True:
        read_from = input('Выберите необходимый пункт меню (0 - для выхода): ')
        if read_from in data_sources:
            print(data_sources[read_from])
            return read_from
        print('Введите "1", "2", "3" или "0" - для выхода из программы')


def load_transactions(read_from: str) -> List[Dict[str, Any]] | None:
    """Загрузка транзакций из файла"""

    source_file_name = get_file_by_drag_and_drop()
    list_transaction = get_transactions_from_file(read_from, source_file_name)

    if list_transaction is None:
        print('Нет транзакций для сортировки')
    return list_transaction


def select_filter_status() -> str:
    """Выбор статуса для фильтрации"""

    unic_state = ['EXECUTED', 'CANCELED', 'PENDING']
    unic_state_lower = [state.lower() for state in unic_state]

    print(f'Доступные для фильтровки статусы: {", ".join(unic_state)}')

    while True:
        filter_str = (
            input(
                f'Введите статус, по которому необходимо выполнить фильтрацию \n'
                f'Доступные для фильтровки статусы: {", ".join(unic_state)}: '
            )
            .strip()
            .lower()
        )

        if filter_str in unic_state_lower:
            original_status = unic_state[unic_state_lower.index(filter_str)]
            print(f"Фильтруем по статусу: {original_status}")
            return original_status
        else:
            print(f'Статус операции "{filter_str}" недоступен')


def apply_date_sorting(sorted_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Применение сортировки по дате"""

    while True:
        date_status = input('Отсортировать операции по дате? Да/Нет: ').strip().lower()

        if date_status == 'нет':
            print('Сортировка по дате не будет применена')
            return sorted_list

        elif date_status == 'да':
            while True:
                sorting_direction = (
                    input('Отсортировать операции по возрастанию или убыванию? ' 'по возрастанию / по убыванию:  ')
                    .strip()
                    .lower()
                )

                if sorting_direction in ['по возрастанию', 'по убыванию']:
                    direction = sorting_direction == 'по убыванию'
                    try:
                        sorted_list = sort_by_date(sorted_list, direction)
                        print('Сортировка по дате применена')
                        return sorted_list
                    except KeyError:
                        print('Не все транзакции содержат дату. Сортировка не возможна.')
                        return sorted_list
                else:
                    print('Выберите направление сортировки')
        else:
            print('Введите "да" или "нет"')


def filter_rub_operations(sorted_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Фильтрация рублевых операций"""

    while True:
        currency_status = input('Выводить только рублевые операции? Да/Нет: ').strip().lower()

        if currency_status == 'нет':
            print('Фильтр по рублевым операциям не будет применен')
            return sorted_list

        if currency_status == 'да':
            try:
                filtered_list = [item for item in sorted_list if item['operationAmount']['currency']['code'] == 'RUB']
                return filtered_list
            except KeyError:
                print('Не все транзакции содержат код валюты. Сортировка не возможна.')
                return sorted_list

        print('Введите "да" или "нет"')


def filter_by_description(
    sorted_list: List[Dict[str, Any]], all_transactions: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Фильтрация по описанию"""

    while True:
        process_status = (
            input('Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ').strip().lower()
        )

        if process_status == 'нет':
            return sorted_list

        if process_status == 'да':
            description_counter = Counter(item.get('description', 'unknown') for item in all_transactions)
            unic_description = list(description_counter.keys())

            search_words = (
                input(
                    f'Введите слово или фразу для поиска (пустая строка - отмена фильтрации). '
                    f'Возможные варианты для фильтрации: {", ".join(str(desc) for desc in unic_description)}: '
                )
                .strip()
                .lower()
            )

            if search_words == '':
                print('Фильтрация по словам не будет применена')
                return sorted_list

            return process_bank_search(sorted_list, search_words)

        else:
            print('Пожалуйста, введите "да" или "нет"')


def display_results(sorted_list: List[Dict[str, Any]], read_from: str):
    """Вывод результатов"""

    if len(sorted_list) > 0:
        print('Вывожу итоговый список транзакций...')
        print(f'Всего банковских операций в выборке: {len(sorted_list)}')

        for transaction in sorted_list:
            if read_from in ['2', '3']:
                handler = output_handler_xlsx_csv(transaction)
            else:
                handler = output_handler_json(transaction)

            print(f'{handler[0]} {handler[1]}\n{handler[2]}\nСумма: {handler[3]} {handler[4]}\n')
    else:
        print('Не найдено ни одной транзакции, подходящей под ваши условия фильтрации')
