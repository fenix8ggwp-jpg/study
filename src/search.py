"""Модуль поиска банковских операций по описанию."""

import re
from typing import Any


def process_bank_search(data: list[dict[str, Any]], search: str) -> list[dict[str, Any]]:
    """Фильтрует банковские операции, в описании которых есть строка поиска.

    Использует библиотеку ``re`` для поиска подстроки без учёта регистра
    в поле ``description`` каждой операции.

    Args:
        data: Список словарей с данными о банковских операциях.
        search: Строка для поиска в описании операции.

    Returns:
        Список словарей с операциями, в описании которых встречается
        переданная строка поиска.
    """
    if not search:
        return list(data)

    pattern = re.compile(re.escape(search), re.IGNORECASE)
    return [
        operation
        for operation in data
        if pattern.search(str(operation.get("description", "")))
    ]