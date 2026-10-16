"""Интеграционные тесты: связка search + operations + main."""

from src.search import process_bank_search
from src.operations import process_bank_operations


def test_search_then_count(sample_operations):
    """Поиск, затем подсчёт по найденным категориям."""
    found = process_bank_search(sample_operations, "Перевод")
    assert len(found) == 4

    counts = process_bank_operations(found, ["Перевод организации"])
    assert counts == {"Перевод организации": 2}


def test_count_all_categories(sample_operations):
    """Подсчёт всех категорий из выборки."""
    categories = [
        "Открытие вклада",
        "Перевод с карты на карту",
        "Перевод организации",
        "Перевод со счета на счет",
    ]
    result = process_bank_operations(sample_operations, categories)
    assert result == {
        "Открытие вклада": 1,
        "Перевод с карты на карту": 1,
        "Перевод организации": 2,
        "Перевод со счета на счет": 1,
    }


def test_search_no_match_then_count(sample_operations):
    """Если поиск ничего не нашёл, подсчёт даёт нули."""
    found = process_bank_search(sample_operations, "несуществующее")
    counts = process_bank_operations(found, ["Перевод организации"])
    assert counts == {"Перевод организации": 0}