from src.logger_config import setup_logger

logger = setup_logger(__name__, "masks.log")


def get_mask_card_number(card_number: str) -> str:
    """Маскирует номер банковской карты.

    Args:
        card_number: Номер карты (16 цифр).

    Returns:
        Строка в формате XXXX XX** **** XXXX.

    Raises:
        ValueError: Если длина номера карты не равна 16 символам.
    """
    logger.debug(f"Вызов get_mask_card_number с аргументом: {card_number}")

    if len(card_number) != 16:
        error_msg = f"Номер карты должен содержать 16 символов, получено: {len(card_number)}"
        logger.error(error_msg)
        raise ValueError(error_msg)

    result = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    logger.info(f"Успешно замаскирован номер карты: {result}")
    return result


def get_mask_account(account_number: str) -> str:
    """Маскирует номер банковского счёта.

    Args:
        account_number: Номер счёта (не менее 4 символов).

    Returns:
        Строка в формате **XXXX.

    Raises:
        ValueError: Если длина номера счёта меньше 4 символов.
    """
    logger.debug(f"Вызов get_mask_account с аргументом: {account_number}")

    if len(account_number) < 4:
        error_msg = (
            f"Номер счета должен содержать не менее 4 символов, получено: {len(account_number)}"
        )
        logger.error(error_msg)
        raise ValueError(error_msg)

    result = f"**{account_number[-4:]}"
    logger.info(f"Успешно замаскирован номер счета: {result}")
    return result
