import pytest


@pytest.fixture
def sample_transactions() -> list[dict]:
    """Фикстура с примерами транзакций разных статусов и дат."""
    return [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]


@pytest.fixture
def sample_transactions_same_date() -> list[dict]:
    """Фикстура с транзакциями с одинаковой датой."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
        {"id": 2, "state": "EXECUTED", "date": "2024-01-01T10:00:00"},
        {"id": 3, "state": "CANCELED", "date": "2024-01-01T10:00:00"},
    ]


@pytest.fixture
def transactions_with_currency() -> list[dict]:
    """Фикстура с транзакциями разных валют."""
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {
                "amount": "43318.34",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {
                "amount": "56883.54",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {
                "amount": "67314.70",
                "currency": {"name": "руб.", "code": "RUB"},
            },
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]

"""Общие фикстуры для всех тестов проекта."""

import json

import pytest


@pytest.fixture
def sample_operations() -> list[dict]:
    """Возвращает небольшой список операций для тестов."""
    return [
        {
            "date": "2019-12-08",
            "description": "Открытие вклада",
            "state": "EXECUTED",
            "amount": "40542 руб.",
            "currency": "RUB",
            "from": "",
            "to": "Счет **4321",
        },
        {
            "date": "2019-11-12",
            "description": "Перевод с карты на карту",
            "state": "EXECUTED",
            "amount": "130 USD",
            "currency": "USD",
            "from": "MasterCard 7771",
            "to": "Visa Platinum 1293",
        },
        {
            "date": "2018-07-18",
            "description": "Перевод организации",
            "state": "EXECUTED",
            "amount": "8390 руб.",
            "currency": "RUB",
            "from": "Visa Platinum 7492",
            "to": "Счет **0034",
        },
        {
            "date": "2018-06-03",
            "description": "Перевод со счета на счет",
            "state": "CANCELED",
            "amount": "8200 EUR",
            "currency": "EUR",
            "from": "Счет **2935",
            "to": "Счет **4321",
        },
        {
            "date": "2020-01-15",
            "description": "Перевод организации",
            "state": "PENDING",
            "amount": "15000 руб.",
            "currency": "RUB",
            "from": "Счет **1111",
            "to": "Счет **2222",
        },
    ]


@pytest.fixture
def json_file(tmp_path, sample_operations):
    """Создаёт временный JSON-файл с операциями."""
    file_path = tmp_path / "operations.json"
    file_path.write_text(
        json.dumps(sample_operations, ensure_ascii=False),
        encoding="utf-8",
    )
    return str(file_path)


@pytest.fixture
def csv_file(tmp_path, sample_operations):
    """Создаёт временный CSV-файл с операциями."""
    import csv

    file_path = tmp_path / "transactions.csv"
    fieldnames = list(sample_operations[0].keys())
    with open(file_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sample_operations)
    return str(file_path)


@pytest.fixture
def xlsx_file(tmp_path, sample_operations):
    """Создаёт временный XLSX-файл с операциями."""
    from openpyxl import Workbook

    file_path = tmp_path / "transactions.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    headers = list(sample_operations[0].keys())
    sheet.append(headers)
    for operation in sample_operations:
        sheet.append([operation[key] for key in headers])
    workbook.save(file_path)
    return str(file_path)