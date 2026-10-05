from collections.abc import Iterator
from typing import Any


def filter_by_currency(
    transactions: list[dict[str, Any]],
    currency_code: str,
) -> Iterator[dict[str, Any]]:
    """Фильтрует транзакции по коду валюты.

    Args:
        transactions: Список словарей с данными о транзакциях.
        currency_code: Код валюты для фильтрации (например, "USD").

    Yields:
        Транзакции, у которых код валюты соответствует заданному.

    Пример:
        >>> transactions = [
        ...     {"operationAmount": {"currency": {"code": "USD"}}},
        ...     {"operationAmount": {"currency": {"code": "RUB"}}},
        ... ]
        >>> list(filter_by_currency(transactions, "USD"))
        [{'operationAmount': {'currency': {'code': 'USD'}}}]
    """
    for transaction in transactions:
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    """Возвращает описания транзакций по очереди.

    Args:
        transactions: Список словарей с данными о транзакциях.

    Yields:
        Описание каждой транзакции.

    Пример:
        >>> transactions = [{"description": "Перевод"}, {"description": "Оплата"}]
        >>> list(transaction_descriptions(transactions))
        ['Перевод', 'Оплата']
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, stop: int) -> Iterator[str]:
    """Генерирует номера банковских карт в заданном диапазоне.

    Args:
        start: Начальное значение диапазона (включительно).
        stop: Конечное значение диапазона (включительно).

    Yields:
        Номер карты в формате XXXX XXXX XXXX XXXX.

    Пример:
        >>> list(card_number_generator(1, 3))
        ['0000 0000 0000 0001', '0000 0000 0000 0002', '0000 0000 0000 0003']
    """
    for number in range(start, stop + 1):
        card_str = str(number).zfill(16)
        yield f"{card_str[:4]} {card_str[4:8]} {card_str[8:12]} {card_str[12:]}"
