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

## Генераторы

### Фильтрация транзакций по валюте

```python
from src.generators import filter_by_currency

usd_transactions = filter_by_currency(transactions, "USD")
for _ in range(2):
    print(next(usd_transactions))

from src.generators import transaction_descriptions

descriptions = transaction_descriptions(transactions)
for _ in range(5):
    print(next(descriptions))

from src.generators import card_number_generator

for card_number in card_number_generator(1, 5):
    print(card_number)
# 0000 0000 0000 0001
# 0000 0000 0000 0002
# ...

## Работа с JSON и API

### Загрузка транзакций из JSON-файла

Функция `load_transactions` читает транзакции из JSON-файла. Если файл не найден, пустой, содержит не-список или некорректный JSON — возвращает пустой список.

```python
from src.utils import load_transactions

transactions = load_transactions("data/operations.json")
print(transactions)
```

### Конвертация валют

Функция `convert_to_rub` принимает транзакцию и возвращает сумму в рублях (float). Если валюта операции — `USD` или `EUR`, происходит обращение к внешнему API за актуальным курсом.

```python
from src.external_api import convert_to_rub

transaction = {
    "operationAmount": {
        "amount": "100",
        "currency": {"code": "USD"},
    }
}
print(convert_to_rub(transaction))  # например, 9000.0
```

### Настройка переменных окружения

1. Скопируйте шаблон `.env.example` в `.env`:
   ```bash
   cp .env.example .env
   ```
2. Заполните переменные:
   - `EXCHANGE_API_KEY` — ключ доступа к API конвертации валют.
   - `EXCHANGE_API_URL` — базовый URL API.

Файл `.env` не попадает в репозиторий (добавлен в `.gitignore`), потому что содержит чувствительные данные.


