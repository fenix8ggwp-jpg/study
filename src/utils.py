import json
from pathlib import Path
from typing import Any


def load_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Пустой список, если:
        - файл не найден;
        - файл пустой;
        - содержимое файла не является списком;
        - файл содержит некорректный JSON.

    Пример:
        >>> load_transactions("data/operations.json")
        [{'id': 441945886, 'state': 'EXECUTED', ...}]
    """
    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return data
