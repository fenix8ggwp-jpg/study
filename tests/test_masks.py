import pytest

from src.masks import get_mask_account, get_mask_card_number


class TestGetMaskCardNumber:
    """Тесты для функции get_mask_card_number."""

    def test_mask_card_number_standard(self) -> None:
        """Маскировка стандартного 16-значного номера карты."""
        assert get_mask_card_number("7000792289606361") == "7000 79** **** 6361"

    @pytest.mark.parametrize(
        "card_number, expected",
        [
            ("1596837868705199", "1596 83** **** 5199"),
            ("7158300734726758", "7158 30** **** 6758"),
            ("6831982476737658", "6831 98** **** 7658"),
            ("8990922113665229", "8990 92** **** 5229"),
            ("5999414228426353", "5999 41** **** 6353"),
        ],
    )
    def test_mask_card_number_multiple_cards(self, card_number: str, expected: str) -> None:
        """Параметризованный тест для разных номеров карт."""
        assert get_mask_card_number(card_number) == expected

    def test_mask_card_number_wrong_length(self) -> None:
        """Ошибка при неверной длине номера карты."""
        with pytest.raises(ValueError, match="Номер карты должен содержать 16 символов"):
            get_mask_card_number("123")


class TestGetMaskAccount:
    """Тесты для функции get_mask_account."""

    def test_mask_account_standard(self) -> None:
        """Маскировка стандартного 20-значного номера счёта."""
        assert get_mask_account("73654108430135874305") == "**4305"

    @pytest.mark.parametrize(
        "account_number, expected",
        [
            ("64686473678894779589", "**9589"),
            ("35383033474447895560", "**5560"),
            ("1234567890", "**7890"),
            ("1234", "**1234"),  # минимальная длина
        ],
    )
    def test_mask_account_multiple_accounts(self, account_number: str, expected: str) -> None:
        """Параметризованный тест для разных номеров счетов."""
        assert get_mask_account(account_number) == expected

    def test_mask_account_too_short(self) -> None:
        """Ошибка при слишком коротком номере счёта."""
        with pytest.raises(ValueError, match="Номер счета должен содержать не менее 4 символов"):
            get_mask_account("123")
