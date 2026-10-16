"""Модуль операций с банковскими транзакциями."""

from collections import Counter
from typing import Any


def process_bank_operations(
    data: list[dict[str, Any]], categories: list[str]
) -> dict[str, int]:
    """Считает количество банковских операций по каждой категории.

    Категория сопоставляется с полем description каждой операции.
    Подсчёт выполняется с помощью collections.Counter.

    Args:
        data: Список словарей с данными о банковских операциях.
        categories: Список названий категорий для подсчёта.

    Returns:
        Словарь, где ключи — названия категорий, а значения — количество
        операций в каждой категории.
    """
    descriptions = [str(operation.get("description", "")) for operation in data]

    counter: Counter[str] = Counter()
    for category_name in categories:
        counter[category_name] = sum(
            1 for description in descriptions if description == category_name
        )

    return dict(counter)