# Bank Widget

Виджет для отображения последних успешных банковских операций клиента.
Проект создан в рамках обучения и демонстрирует работу с Poetry, Git, линтерами и типизацией.

## Возможности

Проект предоставляет следующие функции:

- **Маскировка карт и счетов** — скрывает часть номера для безопасности.
- **Маскировка по типу** — автоматически определяет, карта это или счёт.
- **Форматирование даты** — преобразует ISO-дату в удобный формат.
- **Фильтрация транзакций** — по статусу (`EXECUTED`, `CANCELED` и т.д.).
- **Сортировка транзакций** — по дате (по возрастанию или убыванию).

## Установка

### Требования

- Python 3.11+
- Poetry (устанавливается отдельно)

### Пошаговая инструкция

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/fenix8ggwp-jpg/study.git
   cd study
   
from src.masks import get_mask_card_number, get_mask_account

# Маскировка карты
print(get_mask_card_number("7000792289606361"))
# 7000 79** **** 6361

# Маскировка счёта
print(get_mask_account("73654108430135874305"))
# **4305

from src.widget import mask_account_card, get_date

# Карта
print(mask_account_card("Visa Platinum 7000792289606361"))
# Visa Platinum 7000 79** **** 6361

# Счёт
print(mask_account_card("Счет 73654108430135874305"))
# Счет **4305

# Дата из ISO-формата
print(get_date("2024-03-11T02:26:18.671407"))
# 11.03.2024

from src.processing import filter_by_state, sort_by_date

transactions = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

# Только выполненные транзакции (по умолчанию)
print(filter_by_state(transactions))

# Только отменённые транзакции
print(filter_by_state(transactions, state="CANCELED"))

# Сортировка по дате — от новых к старым (по умолчанию)
print(sort_by_date(transactions))

# Сортировка по дате — от старых к новым
print(sort_by_date(transactions, reverse=False))

## Декоратор log

Декоратор `log` автоматически логирует вызовы функций — имя, результат, ошибки.

### Логирование в консоль

```python
from src.decorators import log

@log()
def add(x, y):
    return x + y

add(1, 2)  # Выведет в консоль: "add ok"