import pytest

from src.widget import get_date, mask_account_card


class TestMaskAccountCard:
    """Тесты для функции mask_account_card."""

    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
            ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
            ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
            ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
            ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ],
    )
    def test_mask_card(self, input_string: str, expected: str) -> None:
        """Универсальность функции для разных типов карт."""
        assert mask_account_card(input_string) == expected

    @pytest.mark.parametrize(
        "input_string, expected",
        [
            ("Счет 73654108430135874305", "Счет **4305"),
            ("Счет 64686473678894779589", "Счет **9589"),
            ("Счет 35383033474447895560", "Счет **5560"),
        ],
    )
    def test_mask_account(self, input_string: str, expected: str) -> None:
        """Функция корректно распознаёт счёт."""
        assert mask_account_card(input_string) == expected

    @pytest.mark.parametrize(
        "invalid_input",
        [
            "",
            "Visa",
            "Visa Platinum Maestro Extra 7000792289606361",
        ],
    )
    def test_invalid_input(self, invalid_input: str) -> None:
        """Ошибка на пустой строке или слишком большом числе подстрок."""
        with pytest.raises(ValueError):
            mask_account_card(invalid_input)


class TestGetDate:
    """Тесты для функции get_date."""

    @pytest.mark.parametrize(
        "date_string, expected",
        [
            ("2024-03-11T02:26:18.671407", "11.03.2024"),
            ("2019-07-03T18:35:29.512364", "03.07.2019"),
            ("2018-06-30T02:08:58.425572", "30.06.2018"),
            ("2000-01-01T00:00:00", "01.01.2000"),
        ],
    )
    def test_get_date_valid(self, date_string: str, expected: str) -> None:
        """Корректное преобразование даты."""
        assert get_date(date_string) == expected

    def test_get_date_invalid(self) -> None:
        """Ошибка на некорректной строке."""
        with pytest.raises(ValueError):
            get_date("not a date")
