from typing import Any, Dict, List


def process_bank_search(data: List[Dict[str, Any]], search: str)->List[Dict[Any, Any]]:

    if not data or not search:
        raise ValueError('Required parameters data or search are empty')

    count = 0
    for item in data:
        if item.get('description'):
            count += 1

    if count == len(data):
        sorted_by_description = [item for item in data if item.get('description') == search]
        return sorted_by_description
    else:
        raise Exception('No data found')