from typing import Any, Dict, List


def filter_by_state(request: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """Функция принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED') и возвращает
    новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению."""

    if not request or not state:
        return []

    count = 0
    for item in request:
        if item.get('state'):
            count += 1

    if count == len(request):
        sorted_by_state = [item for item in request if item.get('state') == state]
        return sorted_by_state
    else:
        return []


def sort_by_date(sorting_data: List[Dict[str, Any]], sorting_direction: bool = True) -> List[Dict[str, Any]]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию —
    убывание). Функция возвращать новый список, отсортированный по дате (date)"""

    if not sorting_data or sorting_direction is not True and sorting_direction is not False:
        return []

    count = 0
    for item in sorting_data:
        if item.get('date'):
            count += 1

    if count == len(sorting_data):
        sorted_by_date = sorted(sorting_data, key=lambda x: x['date'], reverse=sorting_direction)
        return sorted_by_date
    else:
        return []
