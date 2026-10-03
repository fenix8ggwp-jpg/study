import functools
from collections.abc import Callable
from typing import Any


def log(filename: str | None = None) -> Callable:
    """Декоратор для логирования вызовов функций.

    Логирует имя функции и результат при успешном выполнении,
    либо имя функции, тип ошибки и входные параметры при ошибке.

    Args:
        filename: Имя файла для записи логов. Если не указано,
            логи выводятся в консоль.

    Returns:
        Декоратор, оборачивающий функцию.

    Пример:
        >>> @log(filename="mylog.txt")
        ... def my_function(x, y):
        ...     return x + y
        >>> my_function(1, 2)
        # В файле mylog.txt: "my_function ok"
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                _write_log(message, filename)
                return result
            except Exception as error:
                message = (
                    f"{func.__name__} error: {type(error).__name__}. " f"Inputs: {args}, {kwargs}"
                )
                _write_log(message, filename)
                raise

        return wrapper

    return decorator


def _write_log(message: str, filename: str | None) -> None:
    """Записывает сообщение в файл или выводит в консоль.

    Args:
        message: Текст для записи.
        filename: Имя файла. Если None — вывод в консоль.
    """
    if filename:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(message + "\n")
    else:
        print(message)
