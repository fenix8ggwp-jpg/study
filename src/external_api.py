import os
from typing import Any

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_to_rub(transaction: dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли.

    Если валюта операции RUB — возвращает сумму как есть.
    Если USD или EUR — обращается к внешнему API для получения
    актуального курса и конвертирует сумму.

    Args:
        transaction: Словарь с данными о транзакции. Должен содержать
            ключ `operationAmount` с полями `amount` и `currency`.

    Returns:
        Сумма транзакции в рублях (float).

    Raises:
        ValueError: Если структура транзакции некорректна.

    Пример:
        >>> convert_to_rub({"operationAmount": {"amount": "100", "currency": {"code": "RUB"}}})
        100.0
    """
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency_code = transaction["operationAmount"]["currency"]["code"]
    except (KeyError, TypeError, ValueError) as error:
        raise ValueError("Некорректная структура транзакции") from error

    if currency_code == "RUB":
        return amount

    if currency_code not in ("USD", "EUR"):
        raise ValueError(f"Неподдерживаемая валюта: {currency_code}")

    rate = _get_exchange_rate(currency_code)
    return round(amount * rate, 2)


def _get_exchange_rate(currency_code: str) -> float:
    """Получает курс валюты к рублю через внешний API.

    Args:
        currency_code: Код валюты (USD или EUR).

    Returns:
        Курс валюты к рублю.

    Raises:
        ValueError: Если API вернул ошибку или некорректный ответ.
    """
    api_key = os.getenv("EXCHANGE_API_KEY")
    api_url = os.getenv("EXCHANGE_API_URL", "https://api.apilayer.com/exchangerates_data")

    headers = {"apikey": api_key} if api_key else {}
    url = f"{api_url}/latest"
    params = {"base": currency_code, "symbols": "RUB"}

    response = requests.get(url, headers=headers, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()

    try:
        rate = data["rates"]["RUB"]
    except (KeyError, TypeError) as error:
        raise ValueError("API вернул некорректный ответ") from error

    return float(rate)