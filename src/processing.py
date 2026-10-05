from typing import Any


def filter_by_state(
    transactions: list[dict[str, Any]],
    state: str = "EXECUTED",
) -> list[dict[str, Any]]:
    """Фильтрует список транзакций по значению ключа 'state'.

    Args:
        transactions: Список словарей с данными о транзакциях.
        state: Значение ключа 'state' для фильтрации.
            По умолчанию 'EXECUTED'.

    Returns:
        Новый список словарей, у которых 'state' равен указанному значению.

    Пример:
        >>> transactions = [
        ...     {"id": 1, "state": "EXECUTED"},
        ...     {"id": 2, "state": "CANCELED"},
        ...     {"id": 3, "state": "EXECUTED"},
        ... ]
        >>> filter_by_state(transactions)
        [{'id': 1, 'state': 'EXECUTED'}, {'id': 3, 'state': 'EXECUTED'}]
    """

    return [item for item in transactions if item.get("state") == state]


def sort_by_date(
    transactions: list[dict[str, Any]],
    reverse: bool = True,
) -> list[dict[str, Any]]:
    """Сортирует список транзакций по дате.

    Args:
        transactions: Список словарей с данными о транзакциях.
        reverse: Порядок сортировки. True — по убыванию (от новых к старым),
            False — по возрастанию. По умолчанию True.

    Returns:
        Новый отсортированный список словарей.

    Пример:
        >>> transactions = [
        ...     {"id": 1, "date": "2024-01-15T10:00:00"},
        ...     {"id": 2, "date": "2024-03-11T02:26:18"},
        ...     {"id": 3, "date": "2023-12-01T08:30:00"},
        ... ]
        >>> sort_by_date(transactions)
        [{'id': 2, 'date': '2024-03-11T02:26:18'}, ...]
    """
    return sorted(transactions, key=lambda item: item.get("date", ""), reverse=reverse)


if __name__ == "__main__":  # pragma: no cover
    sample_transactions = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

    print("=== Фильтр по state (по умолчанию EXECUTED) ===")
    print(filter_by_state(sample_transactions))

    print("\n=== Фильтр по state (CANCELED) ===")
    print(filter_by_state(sample_transactions, state="CANCELED"))

    print("\n=== Сортировка по дате (по убыванию) ===")
    print(sort_by_date(sample_transactions))

    print("\n=== Сортировка по дате (по возрастанию) ===")
    print(sort_by_date(sample_transactions, reverse=False))
