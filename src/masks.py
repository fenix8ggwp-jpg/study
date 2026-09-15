def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Показывает первые 6 и последние 4 цифры, остальные заменяет на *.

    Args:
        card_number: Номер карты (16 цифр).

    Returns:
        Строка в формате XXXX XX** **** XXXX.

    Пример:
        >>> get_mask_card_number("7000792289606361")
        '7000 79** **** 6361'
    """
    if len(card_number) != 16:
        raise ValueError("Номер карты должен содержать 16 символов")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счета.

    Показывает только последние 4 цифры, перед ними — две звездочки.

    Args:
        account_number: Номер счета (20 цифр).

    Returns:
        Строка в формате **XXXX.

    Пример:
        >>> get_mask_account("73654108430135874305")
        '**4305'
    """
    if len(account_number) < 4:
        raise ValueError("Номер счета должен содержать не менее 4 символов")
    return f"**{account_number[-4:]}"


if __name__ == "__main__":
    print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361
    print(get_mask_account("73654108430135874305"))  # **4305
