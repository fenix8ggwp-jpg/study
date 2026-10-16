"""Тесты для вспомогательных функций и main."""

from unittest.mock import patch

import pytest

from src.main import (
    VALID_STATUSES,
    _ask_yes_no,
    _filter_by_status,
    _filter_rubles,
    _load_csv,
    _load_json,
    _print_operations,
    _sort_by_date,
    main,
)


def test_filter_by_status_is_case_insensitive():
    """Фильтр по статусу нормализует регистр."""
    data = [
        {"state": "EXECUTED", "date": "2020-01-01"},
        {"state": "canceled", "date": "2019-01-01"},
    ]
    assert _filter_by_status(data, "EXECUTED") == [data[0]]


def test_filter_by_status_lowercase_state():
    """Статус в данных в нижнем регистре тоже находится."""
    data = [{"state": "executed"}]
    assert _filter_by_status(data, "EXECUTED") == data


def test_filter_by_status_missing_key():
    """Операции без state не попадают в выборку."""
    data = [{"date": "2020-01-01"}]
    assert _filter_by_status(data, "EXECUTED") == []


def test_filter_by_status_no_matches():
    """Если совпадений нет — пустой список."""
    data = [{"state": "PENDING"}]
    assert _filter_by_status(data, "EXECUTED") == []


@pytest.mark.parametrize("status", VALID_STATUSES)
def test_filter_by_status_all_valid(status):
    """Каждый валидный статус фильтруется корректно."""
    data = [{"state": status}]
    assert _filter_by_status(data, status) == data


def test_sort_by_date_ascending():
    """Сортировка по возрастанию ставит раннюю дату первой."""
    data = [
        {"date": "2020-01-01"},
        {"date": "2019-01-01"},
    ]
    result = _sort_by_date(data, ascending=True)
    assert result[0]["date"] == "2019-01-01"


def test_sort_by_date_descending():
    """Сортировка по убыванию ставит позднюю дату первой."""
    data = [
        {"date": "2019-01-01"},
        {"date": "2020-01-01"},
    ]
    result = _sort_by_date(data, ascending=False)
    assert result[0]["date"] == "2020-01-01"


def test_sort_by_date_empty():
    """Пустой список сортируется без ошибок."""
    assert _sort_by_date([], ascending=True) == []


def test_sort_by_date_does_not_mutate():
    """Исходный список не изменяется."""
    data = [{"date": "2020-01-01"}, {"date": "2019-01-01"}]
    original = list(data)
    _sort_by_date(data, ascending=True)
    assert data == original


def test_filter_rubles():
    """Остаются только рублёвые операции."""
    data = [
        {"currency": "RUB", "amount": "100 руб."},
        {"currency": "USD", "amount": "100 USD"},
    ]
    assert _filter_rubles(data) == [data[0]]


def test_filter_rubles_by_amount_text():
    """Фильтр срабатывает по тексту 'руб' в amount."""
    data = [{"currency": "", "amount": "5000 руб."}]
    assert _filter_rubles(data) == data


def test_filter_rubles_empty():
    """Пустой список — пустой результат."""
    assert _filter_rubles([]) == []


def test_filter_rubles_lowercase_currency():
    """Валюта в нижнем регистре тоже учитывается."""
    data = [{"currency": "rub", "amount": ""}]
    assert _filter_rubles(data) == data


def test_load_json(json_file):
    """JSON-файл читается корректно."""
    result = _load_json(json_file)
    assert isinstance(result, list)
    assert len(result) == 5


def test_load_csv(csv_file):
    """CSV-файл читается корректно."""
    result = _load_csv(csv_file)
    assert isinstance(result, list)
    assert len(result) == 5


def test_ask_yes_no_yes():
    """Ответ 'да' возвращает True."""
    with patch("builtins.input", return_value="да"):
        assert _ask_yes_no("?") is True


def test_ask_yes_no_no():
    """Ответ 'нет' возвращает False."""
    with patch("builtins.input", return_value="нет"):
        assert _ask_yes_no("?") is False


def test_ask_yes_no_retries_on_invalid():
    """Неверный ввод заставляет повторить вопрос."""
    with patch("builtins.input", side_effect=["maybe", "да"]):
        assert _ask_yes_no("?") is True


def test_print_operations_empty(capsys):
    """Пустая выборка печатает сообщение об отсутствии транзакций."""
    _print_operations([])
    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out


def test_print_operations_non_empty(capsys):
    """Непустая выборка печатает количество и сами операции."""
    data = [
        {
            "date": "2019-12-08",
            "description": "Открытие вклада",
            "amount": "40542 руб.",
            "from": "",
        }
    ]
    _print_operations(data)
    captured = capsys.readouterr()
    assert "Всего банковских операций в выборке: 1" in captured.out
    assert "Открытие вклада" in captured.out
    assert "40542 руб." in captured.out


def test_main_full_scenario_json(json_file, capsys):
    """Сквозной сценарий: JSON, статус EXECUTED, без сортировки и фильтров."""
    inputs = iter(["1", "EXECUTED", "нет", "нет", "нет"])
    with patch("builtins.input", side_effect=lambda *_: next(inputs)):
        with patch("src.main._load_json", return_value=[
            {"date": "2019-12-08", "description": "Открытие вклада",
             "state": "EXECUTED", "amount": "40542 руб.", "currency": "RUB",
             "from": "", "to": "Счет **4321"},
        ]):
            main()

    captured = capsys.readouterr()
    assert "Всего банковских операций в выборке: 1" in captured.out
    assert "Открытие вклада" in captured.out


def test_main_invalid_status_retry(capsys):
    """Неверный статус заставляет программу запросить его снова."""
    inputs = iter(["1", "test", "EXECUTED", "нет", "нет", "нет"])
    with patch("builtins.input", side_effect=lambda *_: next(inputs)):
        with patch("src.main._load_json", return_value=[]):
            main()

    captured = capsys.readouterr()
    assert "TEST" in captured.out


def test_main_with_sorting(json_file, capsys):
    """main сортирует по возрастанию, если пользователь согласился."""
    inputs = iter(["1", "EXECUTED", "да", "по возрастанию", "нет", "нет"])
    with patch("builtins.input", side_effect=lambda *_: next(inputs)):
        with patch("src.main._load_json", return_value=[
            {"date": "2020-01-01", "description": "A", "state": "EXECUTED",
             "amount": "1 руб.", "currency": "RUB", "from": "", "to": ""},
            {"date": "2019-01-01", "description": "B", "state": "EXECUTED",
             "amount": "1 руб.", "currency": "RUB", "from": "", "to": ""},
        ]):
            main()

    captured = capsys.readouterr()
    assert captured.out.index("2019-01-01") < captured.out.index("2020-01-01")


def test_main_with_search(json_file, capsys):
    """main фильтрует по слову в описании."""
    inputs = iter(["1", "EXECUTED", "нет", "нет", "да", "Открытие"])
    with patch("builtins.input", side_effect=lambda *_: next(inputs)):
        with patch("src.main._load_json", return_value=[
            {"date": "2019-12-08", "description": "Открытие вклада",
             "state": "EXECUTED", "amount": "40542 руб.", "currency": "RUB",
             "from": "", "to": ""},
            {"date": "2019-11-12", "description": "Перевод",
             "state": "EXECUTED", "amount": "130 USD", "currency": "USD",
             "from": "", "to": ""},
        ]):
            main()

    captured = capsys.readouterr()
    assert "Открытие вклада" in captured.out
    assert "Перевод" not in captured.out


def test_main_with_ruble_filter(json_file, capsys):
    """main оставляет только рублёвые транзакции."""
    inputs = iter(["1", "EXECUTED", "нет", "да", "нет"])
    with patch("builtins.input", side_effect=lambda *_: next(inputs)):
        with patch("src.main._load_json", return_value=[
            {"date": "2019-12-08", "description": "A",
             "state": "EXECUTED", "amount": "100 руб.", "currency": "RUB",
             "from": "", "to": ""},
            {"date": "2019-11-12", "description": "B",
             "state": "EXECUTED", "amount": "130 USD", "currency": "USD",
             "from": "", "to": ""},
        ]):
            main()

    captured = capsys.readouterr()
    assert "A" in captured.out
    assert "B" not in captured.out


def test_main_empty_result(json_file, capsys):
    """Если выборка пустая — выводится сообщение."""
    inputs = iter(["1", "PENDING", "нет", "нет", "нет"])
    with patch("builtins.input", side_effect=lambda *_: next(inputs)):
        with patch("src.main._load_json", return_value=[
            {"date": "2019-12-08", "description": "A",
             "state": "EXECUTED", "amount": "100 руб.", "currency": "RUB",
             "from": "", "to": ""},
        ]):
            main()

    captured = capsys.readouterr()
    assert "Не найдено ни одной транзакции" in captured.out


def test_main_csv_choice(csv_file, capsys):
    """Выбор пункта 2 загружает CSV-файл."""
    inputs = iter(["2", "EXECUTED", "нет", "нет", "нет"])
    with patch("builtins.input", side_effect=lambda *_: next(inputs)):
        with patch("src.main._load_csv", return_value=[]):
            main()

    captured = capsys.readouterr()
    assert "Для обработки выбран CSV-файл." in captured.out