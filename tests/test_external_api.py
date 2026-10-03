from unittest.mock import MagicMock, patch

import pytest

from src.external_api import convert_to_rub


class TestConvertToRub:
    """Тесты для функции convert_to_rub."""

    def test_rub_transaction(self) -> None:
        """RUB — возвращается сумма как есть, без запроса к API."""
        transaction = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "RUB"},
            }
        }
        assert convert_to_rub(transaction) == 1000.50

    @patch("src.external_api.requests.get")
    def test_usd_transaction(self, mock_get: MagicMock) -> None:
        """USD — конвертация через API."""
        mock_get.return_value.json.return_value = {"rates": {"RUB": 90.0}}
        mock_get.return_value.raise_for_status = MagicMock()

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"},
            }
        }
        assert convert_to_rub(transaction) == 9000.0

    @patch("src.external_api.requests.get")
    def test_eur_transaction(self, mock_get: MagicMock) -> None:
        """EUR — конвертация через API."""
        mock_get.return_value.json.return_value = {"rates": {"RUB": 100.0}}
        mock_get.return_value.raise_for_status = MagicMock()

        transaction = {
            "operationAmount": {
                "amount": "50",
                "currency": {"code": "EUR"},
            }
        }
        assert convert_to_rub(transaction) == 5000.0

    def test_invalid_structure(self) -> None:
        """Некорректная структура — ValueError."""
        with pytest.raises(ValueError, match="Некорректная структура"):
            convert_to_rub({})

    def test_unsupported_currency(self) -> None:
        """Неподдерживаемая валюта — ValueError."""
        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "GBP"},
            }
        }
        with pytest.raises(ValueError, match="Неподдерживаемая валюта"):
            convert_to_rub(transaction)

    @patch("src.external_api.requests.get")
    def test_api_invalid_response(self, mock_get: MagicMock) -> None:
        """API вернул некорректный ответ — ValueError."""
        mock_get.return_value.json.return_value = {"error": "something"}
        mock_get.return_value.raise_for_status = MagicMock()

        transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {"code": "USD"},
            }
        }
        with pytest.raises(ValueError, match="API вернул некорректный ответ"):
            convert_to_rub(transaction)
