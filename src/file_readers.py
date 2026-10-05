from pathlib import Path
from typing import Any, cast

import pandas as pd

from src.logger_config import setup_logger

logger = setup_logger(__name__, "file_readers.log")


def read_csv_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла.

    Args:
        file_path: Путь к CSV-файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Пустой список, если файл
        не найден или пустой.
    """
    logger.debug(f"Попытка загрузить транзакции из CSV: {file_path}")

    try:
        df = pd.read_csv(file_path, encoding="utf-8", sep=";")
    except FileNotFoundError:
        logger.error(f"Файл CSV не найден: {file_path}")
        return []
    except pd.errors.EmptyDataError:
        logger.error(f"CSV-файл пустой: {file_path}")
        return []

    if df.empty:
        logger.info(f"CSV-файл пустой: {file_path}")
        return []

    transactions = cast(list[dict[str, Any]], df.to_dict(orient="records"))
    logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV")
    return transactions


def read_excel_transactions(file_path: str | Path) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла (.xlsx).

    Args:
        file_path: Путь к Excel-файлу с транзакциями.

    Returns:
        Список словарей с транзакциями. Пустой список, если файл
        не найден или пустой.
    """
    logger.debug(f"Попытка загрузить транзакции из Excel: {file_path}")

    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except FileNotFoundError:
        logger.error(f"Excel-файл не найден: {file_path}")
        return []

    if df.empty:
        logger.info(f"Excel-файл пустой: {file_path}")
        return []

    transactions = cast(list[dict[str, Any]], df.to_dict(orient="records"))
    logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel")
    return transactions
