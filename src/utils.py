import json
from pathlib import Path
from typing import Any

from src.logger_config import setup_logger

logger = setup_logger(__name__, "utils.log")


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
    """
    logger.debug(f"Попытка загрузить транзакции из файла: {file_path}")

    try:
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as error:
        logger.error(f"Некорректный JSON в файле {file_path}: {error}")
        return []

    if not isinstance(data, list):
        logger.error(f"Данные в файле {file_path} не являются списком")
        return []

    logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
    return data
