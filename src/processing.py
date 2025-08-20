from typing import Any, Dict, List


def filter_by_state(request: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """Функция принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED') и возвращает
    новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению."""

    sorted_by_state = [item for item in request if item.get('state') == state]

    return sorted_by_state


def sort_by_date(sorting_data: List[Dict[str, Any]], sorting_direction: bool = True) -> List[Dict[str, Any]]:
    """Функция принимает список словарей и необязательный параметр, задающий порядок сортировки (по умолчанию —
    убывание). Функция должна возвращать новый список, отсортированный по дате (date)"""

    sorted_by_date = sorted(sorting_data, key=lambda x: x['date'], reverse=sorting_direction)

    return sorted_by_date
