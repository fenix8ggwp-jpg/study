import json
from pathlib import Path

import pytest

from src.utils import load_transactions


class TestLoadTransactions:
    """Тесты для функции load_transactions."""

    def test_load_valid_file(self, tmp_path: Path) -> None:
        """Чтение корректного JSON-файла."""
        file_path = tmp_path / "valid.json"
        transactions = [{"id": 1, "amount": 100}]
        file_path.write_text(json.dumps(transactions), encoding="utf-8")

        result = load_transactions(str(file_path))
        assert result == transactions

    def test_load_nonexistent_file(self, tmp_path: Path) -> None:
        """Несуществующий файл — пустой список."""
        file_path = tmp_path / "nonexistent.json"
        assert load_transactions(str(file_path)) == []

    def test_load_empty_file(self, tmp_path: Path) -> None:
        """Пустой файл — пустой список."""
        file_path = tmp_path / "empty.json"
        file_path.write_text("", encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_load_invalid_json(self, tmp_path: Path) -> None:
        """Некорректный JSON — пустой список."""
        file_path = tmp_path / "invalid.json"
        file_path.write_text("{not valid json", encoding="utf-8")
        assert load_transactions(str(file_path)) == []

    def test_load_non_list_json(self, tmp_path: Path) -> None:
        """JSON не является списком — пустой список."""
        file_path = tmp_path / "dict.json"
        file_path.write_text('{"key": "value"}', encoding="utf-8")
        assert load_transactions(str(file_path)) == []