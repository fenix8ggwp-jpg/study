import pytest

from src.generators import (
    card_number_generator,
    filter_by_currency,
    transaction_descriptions,
)


class TestFilterByCurrency:
    """Тесты для функции filter_by_currency."""

    def test_filter_usd(self, transactions_with_currency: list[dict]) -> None:
        """Фильтрация USD-транзакций."""
        result = list(filter_by_currency(transactions_with_currency, "USD"))
        assert len(result) == 3
        assert all(tx["operationAmount"]["currency"]["code"] == "USD" for tx in result)

    def test_filter_rub(self, transactions_with_currency: list[dict]) -> None:
        """Фильтрация RUB-транзакций."""
        result = list(filter_by_currency(transactions_with_currency, "RUB"))
        assert len(result) == 2

    def test_filter_no_match(self, transactions_with_currency: list[dict]) -> None:
        """Пустой результат, если валюты нет."""
        result = list(filter_by_currency(transactions_with_currency, "EUR"))
        assert result == []

    def test_filter_empty_list(self) -> None:
        """Пустой список — пустой результат."""
        assert list(filter_by_currency([], "USD")) == []

    def test_filter_returns_iterator(self, transactions_with_currency: list[dict]) -> None:
        """Функция возвращает итератор."""
        result = filter_by_currency(transactions_with_currency, "USD")
        assert iter(result) is result


class TestTransactionDescriptions:
    """Тесты для функции transaction_descriptions."""

    def test_descriptions_correct(self, transactions_with_currency: list[dict]) -> None:
        """Правильные описания по очереди."""
        result = list(transaction_descriptions(transactions_with_currency))
        assert result == [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации",
        ]

    def test_descriptions_empty(self) -> None:
        """Пустой список — пустой результат."""
        assert list(transaction_descriptions([])) == []

    def test_descriptions_missing_key(self) -> None:
        """Транзакции без description возвращают пустую строку."""
        transactions: list[dict] = [{"id": 1}, {"description": "Оплата"}]
        assert list(transaction_descriptions(transactions)) == ["", "Оплата"]


class TestCardNumberGenerator:
    """Тесты для генератора card_number_generator."""

    @pytest.mark.parametrize(
        "start, stop, expected",
        [
            (
                1,
                3,
                [
                    "0000 0000 0000 0001",
                    "0000 0000 0000 0002",
                    "0000 0000 0000 0003",
                ],
            ),
            (
                9999,
                10001,
                [
                    "0000 0000 0000 9999",
                    "0000 0000 0001 0000",
                    "0000 0000 0001 0001",
                ],
            ),
        ],
    )
    def test_card_numbers(self, start: int, stop: int, expected: list[str]) -> None:
        """Корректные номера в диапазоне."""
        assert list(card_number_generator(start, stop)) == expected

    def test_card_number_format(self) -> None:
        """Номер карты в правильном формате."""
        result = list(card_number_generator(1, 1))[0]
        assert len(result) == 19  # 16 цифр + 3 пробела
        assert result.count(" ") == 3

    def test_card_number_max_value(self) -> None:
        """Максимальное значение диапазона."""
        result = list(card_number_generator(9999999999999999, 9999999999999999))
        assert result == ["9999 9999 9999 9999"]
