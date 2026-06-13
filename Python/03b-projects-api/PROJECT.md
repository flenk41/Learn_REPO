# 🚀 Мини-проект — CLI-клиент для веб-API (погода/GitHub)

> 🎯 **Цель:** собрать **настоящий проект-пакет**, который объединяет обе грани API:
> ты **используешь** чужой веб-API и **проектируешь** свой чистый клиент поверх него — со
> структурой, типами, тестами и точкой входа.

---

## 📋 Что делаем

Консольную утилиту, которая запрашивает данные из веб-API и красиво выводит. Например —
погода по городу или информация о пользователе GitHub:

```bash
$ python -m weathercli Москва
📍 Москва
🌡️  Температура: 18°C (ощущается 16°C)
💨 Ветер: 4 м/с
☁️  Облачно
```

(можно выбрать любой открытый API: open-meteo для погоды — без ключа, или GitHub).

---

## 📂 Требуемая структура

```
weathercli/
├── src/
│   └── weathercli/
│       ├── __init__.py        ← публичный API пакета (__all__, __version__)
│       ├── __main__.py        ← точка входа: python -m weathercli
│       ├── client.py          ← клиент API (свой чистый интерфейс)
│       ├── models.py          ← @dataclass Weather / City
│       └── errors.py          ← свои исключения
├── tests/
│   └── test_client.py
├── pyproject.toml
├── requirements.txt           ← requests
└── README.md
```

---

## ✅ Требования (минимум)

- [ ] Структура **пакета** (`src/weathercli/`), запуск через `python -m weathercli`.
- [ ] **Класс-клиент** (`WeatherClient`) с чистым API: публичные методы + `_приватные`
      помощники, скрытая работа с `requests`.
- [ ] **Типы** на всех публичных функциях, результат — `@dataclass` (модели).
- [ ] **Свои исключения** (`CityNotFound`, `ApiError`) вместо None/print.
- [ ] Обработка ошибок: timeout, нет сети, плохой код ответа.
- [ ] Ключи (если есть) — из переменных окружения, не из кода.
- [ ] Хотя бы 2–3 теста (pytest) — можно с «замоканным» ответом.
- [ ] `README.md` с установкой и примером.

---

## 🪜 Пошаговый план

1. **API-first.** Сначала спроектируй интерфейс клиента (модуль 2): какие методы нужны?
   `get_weather(city: str) -> Weather`. Запиши в `client.py` сигнатуры и docstring.
2. **Модели.** В `models.py` — `@dataclass Weather` (temp, feels_like, wind, description).
3. **Исключения.** В `errors.py` — `CityNotFound`, `ApiError`.
4. **Реализация клиента.** В `client.py` — `requests.Session`, таймаут, `raise_for_status`,
   парсинг JSON в `Weather`. Приватные `_request`, `_parse`.
5. **CLI.** В `__main__.py` — взять город из `sys.argv`, вызвать клиент, красиво вывести,
   поймать исключения.
6. **Пакет.** `__init__.py` с `__all__`, `__version__`. `pyproject.toml`.
7. **Тесты.** Проверь парсинг и обработку ошибок (можно подменять ответ).

---

## 🧱 Скелеты

**src/weathercli/models.py:**
```python
from dataclasses import dataclass

@dataclass
class Weather:
    city: str
    temp: float
    feels_like: float
    wind: float
    description: str
```

**src/weathercli/errors.py:**
```python
class WeatherError(Exception):
    """Базовая ошибка пакета."""

class CityNotFound(WeatherError):
    """Город не найден."""

class ApiError(WeatherError):
    """Сервис вернул ошибку."""
```

**src/weathercli/client.py:**
```python
import requests
from .models import Weather
from .errors import CityNotFound, ApiError

class WeatherClient:
    """Клиент погодного API. Скрывает работу с сетью за чистым интерфейсом."""

    def __init__(self, timeout: int = 10):
        self._session = requests.Session()
        self._timeout = timeout

    def get_weather(self, city: str) -> Weather:
        """Получить погоду по названию города.

        Raises:
            CityNotFound: если город не найден.
            ApiError: при ошибке сервиса/сети.
        """
        coords = self._geocode(city)         # приватный помощник
        if coords is None:
            raise CityNotFound(f"Город не найден: {city}")
        return self._fetch_weather(city, coords)

    def _geocode(self, city: str):
        # запрос к geocoding API → (lat, lon) или None   (реализуй)
        ...

    def _fetch_weather(self, city, coords) -> Weather:
        # запрос к weather API → Weather   (реализуй)
        ...
```

**src/weathercli/__main__.py:**
```python
import sys
from .client import WeatherClient
from .errors import WeatherError

def main():
    if len(sys.argv) < 2:
        print("Использование: python -m weathercli <город>")
        return
    city = sys.argv[1]
    try:
        w = WeatherClient().get_weather(city)
        print(f"📍 {w.city}\n🌡️  {w.temp}°C (ощущается {w.feels_like}°C)")
        print(f"💨 Ветер: {w.wind} м/с\n☁️  {w.description}")
    except WeatherError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
```

> 💡 Открытый API без ключа: **open-meteo.com** (geocoding + forecast). Изучи его
> документацию — это тоже навык «читать чужой API».

---

## 💪 Усложнения (для «отлично»)

- ➕ Прогноз на несколько дней.
- ➕ Кэш ответов (чтобы не дёргать API повторно) — словарь или файл.
- ➕ Аргументы через `argparse` (флаги `--days`, `--units`).
- ➕ Команда в системе через `[project.scripts]` в pyproject (`weather Москва`).
- ➕ Полное покрытие тестами с подменой сети (`unittest.mock` / `responses`).
- ➕ Типы строго проходят `mypy`, код чист по `ruff`.

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | Пакет + клиент с чистым API + типы + исключения + обработка ошибок + запуск |
| 🌟 Хорошо | + тесты, кэш или argparse, README |
| 🏆 Отлично | + mypy/ruff чисто, мок-тесты, команда через pyproject |

---

## 🎓 Чему ты научился

Ты собрал полноценный проект, который **использует чужой веб-API** и **предоставляет свой
чистый API** поверх него — со структурой пакета, типами, исключениями и тестами. Это
типовая архитектура реальных Python-инструментов и SDK.

Сохрани в `my-code/Python/weathercli/`. 🎉

➡️ Назад к [разделу](README.md) · [дорожной карте Python](../README.md)
