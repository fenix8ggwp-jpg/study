import logging
from logging import FileHandler, Formatter, Logger
from pathlib import Path


def setup_logger(name: str, log_file: str) -> Logger:
    """Создаёт и настраивает логер для модуля.

    Args:
        name: Имя логера (обычно __name__ модуля).
        log_file: Имя файла для записи логов (без пути).

    Returns:
        Настроенный объект Logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    logs_dir = Path(__file__).resolve().parent.parent / "logs"
    logs_dir.mkdir(exist_ok=True)

    log_path = logs_dir / log_file

    file_handler = FileHandler(log_path, mode="w", encoding="utf-8")

    file_formatter = Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger
