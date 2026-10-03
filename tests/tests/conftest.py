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
