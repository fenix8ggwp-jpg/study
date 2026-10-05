import pytest

from src.processing import filter_by_state, sort_by_date


class TestFilterByState:
    """Тесты для функции filter_by_state."""

    def test_filter_default_executed(self, sample_transactions: list[dict]) -> None:
        """По умолчанию фильтрует по EXECUTED."""
        result = filter_by_state(sample_transactions)
        assert len(result) == 2
        assert all(item["state"] == "EXECUTED" for item in result)

    def test_filter_by_canceled(self, sample_transactions: list[dict]) -> None:
        """Фильтрация по CANCELED."""
        result = filter_by_state(sample_transactions, state="CANCELED")
        assert len(result) == 2
        assert all(item["state"] == "CANCELED" for item in result)

    @pytest.mark.parametrize("state", ["PENDING", "FAILED", "UNKNOWN"])
    def test_filter_empty_result(self, sample_transactions: list[dict], state: str) -> None:
        """Пустой список, если такого статуса нет."""
        assert filter_by_state(sample_transactions, state=state) == []

    def test_filter_empty_list(self) -> None:
        """Фильтрация пустого списка."""
        assert filter_by_state([]) == []


class TestSortByDate:
    """Тесты для функции sort_by_date."""

    def test_sort_descending(self, sample_transactions: list[dict]) -> None:
        """Сортировка по убыванию (по умолчанию)."""
        result = sort_by_date(sample_transactions)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_ascending(self, sample_transactions: list[dict]) -> None:
        """Сортировка по возрастанию."""
        result = sort_by_date(sample_transactions, reverse=False)
        dates = [item["date"] for item in result]
        assert dates == sorted(dates)

    def test_sort_same_dates(self, sample_transactions_same_date: list[dict]) -> None:
        """Сортировка с одинаковыми датами — не падает."""
        result = sort_by_date(sample_transactions_same_date)
        assert len(result) == 3

    def test_sort_empty_list(self) -> None:
        """Сортировка пустого списка."""
        assert sort_by_date([]) == []
