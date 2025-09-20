import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str) -> List[Dict[str, Any]]:
    """Функция для поиска в списке словарей операций по заданной строке возвращает список словарей с операциями, у
    которых в описании есть строка, переданная аргументу функции"""

    if not data:
        raise ValueError('Data cannot be empty')
    if not search:
        raise ValueError('Search query cannot be empty')

    pattern = re.compile(search, re.IGNORECASE)
    sorted_by_description = [item for item in data if pattern.search(item.get('description', ''))]

    return sorted_by_description


def process_bank_classification(data: List[Dict[str, Any]], classification: List[str]) -> Dict[str, Any]:
    """Функция для подсчета количества банковских операций определенного типа возвращает словарь, в котором ключи —
    это названия категорий, а значения — это количество операций в каждой категории"""

    if not data:
        raise ValueError('Data cannot be empty')
    if not classification:
        raise ValueError('Search query cannot be empty')

    sorted_by_description = [item for item in data if item.get('description') in classification]
    descriptions = [item['description'] for item in sorted_by_description]
    statistics_dict = Counter(descriptions)

    return dict(statistics_dict)
