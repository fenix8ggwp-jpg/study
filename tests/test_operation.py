"""Тесты для process_bank_operation."""

import pytest

from src.operations import process_bank_operations

SAMPLE = [
    {"description": "Перевод организации"},
    {"description": "Перевод организации"},
    {"description": "Открытие вклада"},
    {"description": "Перевод с карты на карту"},
]


def test_counts_categories():
    """Корректно считает каждую запрошенную категорию."""
    result = process_bank_operations(
        SAMPLE, ["Перевод организации", "Открытие вклада"]
    )
    assert result == {"Перевод организации": 2, "Открытие вклада": 1}


def test_missing_category_returns_zero():
    """Отсутствующая категория возвращает ноль."""
    result = process_bank_operations(SAMPLE, ["Неизвестно"])
    assert result == {"Неизвестно": 0}


def test_empty_data():
    """Пустые данные возвращают нули для всех категорий."""
    result = process_bank_operations([], ["A", "B"])
    assert result == {"A": 0, "B": 0}


def test_empty_categories():
    """Пустой список категорий возвращает пустой словарь."""
    assert process_bank_operations(SAMPLE, []) == {}


def test_both_empty():
    """Оба аргумента пустые — пустой словарь."""
    assert process_bank_operations([], []) == {}


def test_duplicate_categories_in_request():
    """Дубликаты в списке категорий схлопываются."""
    result = process_bank_operations(
        SAMPLE, ["Перевод организации", "Перевод организации"]
    )
    assert result == {"Перевод организации": 2}


def test_case_sensitive_counting():
    """Подсчёт учитывает регистр описания."""
    data = [
        {"description": "Перевод"},
        {"description": "перевод"},
    ]
    result = process_bank_operations(data, ["Перевод", "перевод"])
    assert result == {"Перевод": 1, "перевод": 1}


def test_missing_description_key():
    """Операции без description не падают с ошибкой."""
    data = [{"state": "EXECUTED"}, {"description": "Перевод"}]
    result = process_bank_operations(data, ["Перевод"])
    assert result == {"Перевод": 1}


def test_returns_dict_type():
    """Возвращаемый объект — словарь."""
    result = process_bank_operations(SAMPLE, ["Открытие вклада"])
    assert isinstance(result, dict)


@pytest.mark.parametrize(
    "categories,expected",
    [
        (["Перевод организации"], {"Перевод организации": 2}),
        (
            ["Перевод организации", "Открытие вклада"],
            {"Перевод организации": 2, "Открытие вклада": 1},
        ),
        (["Перевод с карты на карту"], {"Перевод с карты на карту": 1}),
        (["Нет такой"], {"Нет такой": 0}),
    ],
)
def test_count_parametrized(categories, expected):
    """Параметризованная проверка подсчёта."""
    assert process_bank_operations(SAMPLE, categories) == expected