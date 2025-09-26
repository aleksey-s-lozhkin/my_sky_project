from typing import Any, Dict, List

from src.processing import filter_by_state
from src.user_interaction import (
    apply_date_sorting,
    display_results,
    filter_by_description,
    filter_rub_operations,
    load_transactions,
    select_data_source,
    select_filter_status,
)


def main() -> List[Dict[str, Any]] | None:
    """Функция отвечает за основную логику проекта, взаимодействие с пользователем и связывает функциональности
    между собой."""

    # Выбор источника данных
    read_from = select_data_source()
    if read_from == '0':
        return None

    # Загрузка транзакций
    list_transaction = load_transactions(read_from)
    if list_transaction is None:
        return None

    # Фильтрация по статусу
    filter_status = select_filter_status()
    try:
        sorted_list = filter_by_state(list_transaction, filter_status)
    except ValueError as err:
        print(f'Ошибка: {err}')
        return None

    # Применение различных фильтров и сортировок
    sorted_list = apply_date_sorting(sorted_list)
    sorted_list = filter_rub_operations(sorted_list)
    sorted_list = filter_by_description(sorted_list)

    # Вывод результатов
    display_results(sorted_list, read_from)

    return sorted_list


# Запуск программы
operation_start = main()
if operation_start is not None:
    print('Работа программы завершена успешно')
else:
    print('Работа программы завершена')
