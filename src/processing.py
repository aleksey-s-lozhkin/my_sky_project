from typing import List, Dict, Any

def filter_by_state(request: List[Dict[str, Any]], state: str = 'EXECUTED') -> List[Dict[str, Any]]:
    """Функция принимает список словарей и опционально значение для ключа state (по умолчанию 'EXECUTED') и возвращает
    новый список словарей, содержащий только те словари, у которых ключ state соответствует указанному значению."""

    sorted_by_state = [item for item in request if item.get('state') == state]

    return sorted_by_state