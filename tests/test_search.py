"""Тесты для process_bank_search."""

import pytest

from src.search import process_bank_search

SAMPLE = [
    {"description": "Перевод организации", "state": "EXECUTED"},
    {"description": "Открытие вклада", "state": "EXECUTED"},
    {"description": "Перевод с карты на карту", "state": "CANCELED"},
]


def test_search_matches_substring():
    """Поиск возвращает операции, содержащие подстроку."""
    assert len(process_bank_search(SAMPLE, "Перевод")) == 2


def test_search_is_case_insensitive():
    """Поиск не учитывает регистр."""
    assert len(process_bank_search(SAMPLE, "перевод")) == 2


def test_search_uppercase_query():
    """Поиск в верхнем регистре тоже работает."""
    assert len(process_bank_search(SAMPLE, "ПЕРЕВОД")) == 2


def test_search_no_matches():
    """Поиск возвращает пустой список, если совпадений нет."""
    assert process_bank_search(SAMPLE, "xyz") == []


def test_search_empty_string_returns_all():
    """Пустая строка поиска возвращает все операции."""
    assert process_bank_search(SAMPLE, "") == SAMPLE


def test_search_none_string_returns_all():
    """None вместо строки поиска возвращает все операции."""
    assert process_bank_search(SAMPLE, None) == SAMPLE


def test_search_special_chars_are_escaped():
    """Спецсимволы регулярных выражений обрабатываются буквально."""
    data = [{"description": "Payment (test)"}]
    assert process_bank_search(data, "(test)") == data


def test_search_dot_is_literal():
    """Точка в поиске не является 'любым символом'."""
    data = [
        {"description": "abc.def"},
        {"description": "abcXdef"},
    ]
    result = process_bank_search(data, "abc.def")
    assert len(result) == 1
    assert result[0]["description"] == "abc.def"


def test_search_missing_description_key():
    """Операции без поля description не падают с ошибкой."""
    data = [{"state": "EXECUTED"}, {"description": "Перевод"}]
    assert len(process_bank_search(data, "Перевод")) == 1


def test_search_empty_data():
    """Пустой список операций возвращает пустой список."""
    assert process_bank_search([], "Перевод") == []


def test_search_partial_word():
    """Поиск по части слова тоже работает."""
    assert len(process_bank_search(SAMPLE, "кл")) == 1


@pytest.mark.parametrize(
    "query,expected_count",
    [
        ("Перевод", 2),
        ("Открытие", 1),
        ("карты", 1),
        ("не найдено", 0),
        ("", 3),
    ],
)
def test_search_parametrized(query, expected_count):
    """Параметризованная проверка разных запросов."""
    assert len(process_bank_search(SAMPLE, query)) == expected_count