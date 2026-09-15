from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """Маскирует номер карты или счета в зависимости от типа.

    Args:
        account_info: Строка с типом и номером, например
            "Visa Platinum 7000792289606361" или "Счет 73654108430135874305".

    Returns:
        Строка с замаскированным номером и исходным типом.

    Raises:
        ValueError: Если строка не содержит номера или содержит больше 3 подстрок.

    Пример:
        >>> mask_account_card("Visa Platinum 7000792289606361")
        'Visa Platinum 7000 79** **** 6361'
        >>> mask_account_card("Счет 73654108430135874305")
        'Счет **4305'
    """
    parts = account_info.split()
    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер")
    if len(parts) > 3:
        raise ValueError("Строка содержит слишком много подстрок")

    number = parts[-1]
    name = " ".join(parts[:-1])

    if "счет" in name.lower() or "account" in name.lower():
        masked = get_mask_account(number)
    else:
        masked = get_mask_card_number(number)

    return f"{name} {masked}"


def get_date(date_string: str) -> str:
    """Преобразует дату из ISO-формата в формат ДД.ММ.ГГГГ.

    Args:
        date_string: Строка с датой в формате "2024-03-11T02:26:18.671407".

    Returns:
        Строка с датой в формате "11.03.2024".

    Пример:
        >>> get_date("2024-03-11T02:26:18.671407")
        '11.03.2024'
    """
    date_obj = datetime.fromisoformat(date_string)
    return date_obj.strftime("%d.%m.%Y")


if __name__ == "__main__":
    print(mask_account_card("Visa Platinum 7000792289606361"))
    print(mask_account_card("Счет 73654108430135874305"))
    print(get_date("2024-03-11T02:26:18.671407"))
