from unittest.mock import MagicMock, patch

import pandas as pd

from src.file_readers import read_csv_transactions, read_excel_transactions


class TestReadCsvTransactions:
    """Тесты для read_csv_transactions."""

    @patch("src.file_readers.pd.read_csv")
    def test_read_csv_success(self, mock_read_csv: MagicMock) -> None:
        """Успешное чтение CSV."""
        mock_df = pd.DataFrame([{"id": 1, "amount": 100}, {"id": 2, "amount": 200}])
        mock_read_csv.return_value = mock_df

        result = read_csv_transactions("dummy.csv")
        assert len(result) == 2
        assert result[0]["id"] == 1

    @patch("src.file_readers.pd.read_csv")
    def test_read_csv_empty(self, mock_read_csv: MagicMock) -> None:
        """Пустой CSV — пустой список."""
        mock_read_csv.return_value = pd.DataFrame()
        assert read_csv_transactions("empty.csv") == []

    @patch("src.file_readers.pd.read_csv", side_effect=FileNotFoundError)
    def test_read_csv_not_found(self, mock_read_csv: MagicMock) -> None:
        """Файл не найден — пустой список."""
        assert read_csv_transactions("missing.csv") == []

    @patch("src.file_readers.pd.read_csv", side_effect=pd.errors.EmptyDataError)
    def test_read_csv_empty_data_error(self, mock_read_csv: MagicMock) -> None:
        """EmptyDataError — пустой список."""
        assert read_csv_transactions("bad.csv") == []


class TestReadExcelTransactions:
    """Тесты для read_excel_transactions."""

    @patch("src.file_readers.pd.read_excel")
    def test_read_excel_success(self, mock_read_excel: MagicMock) -> None:
        """Успешное чтение Excel."""
        mock_df = pd.DataFrame([{"id": 1, "amount": 100}])
        mock_read_excel.return_value = mock_df

        result = read_excel_transactions("dummy.xlsx")
        assert len(result) == 1
        assert result[0]["id"] == 1

    @patch("src.file_readers.pd.read_excel")
    def test_read_excel_empty(self, mock_read_excel: MagicMock) -> None:
        """Пустой Excel — пустой список."""
        mock_read_excel.return_value = pd.DataFrame()
        assert read_excel_transactions("empty.xlsx") == []

    @patch("src.file_readers.pd.read_excel", side_effect=FileNotFoundError)
    def test_read_excel_not_found(self, mock_read_excel: MagicMock) -> None:
        """Файл не найден — пустой список."""
        assert read_excel_transactions("missing.xlsx") == []
