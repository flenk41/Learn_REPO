# 🚀 Пет-проект уровня 3 — Менеджер библиотеки (ООП + JSON)

> 🎯 **Цель:** собрать всё из Middle — классы, исключения, файлы/JSON, модули — в одно
> приложение с понятной архитектурой. Это уже «портфолио-проект».

---

## 📋 Что должна уметь программа

Консольный менеджер библиотеки книг с сохранением между запусками:

```
==== БИБЛИОТЕКА ====
1. Показать все книги
2. Добавить книгу
3. Выдать книгу читателю
4. Вернуть книгу
5. Поиск
6. Статистика
0. Выход (с сохранением)
> 1

📚 Книги (3):
[1] "1984" — Оруэлл (1949) ✅ доступна
[2] "Война и мир" — Толстой (1869) 📕 у читателя: Гена
[3] "Понимание C" — ... (2020) ✅ доступна
```

---

## ✅ Требования (минимум)

- [ ] Классы `Book` и `Library` (ООП), методы для всех операций.
- [ ] Хранение книг в коллекции (список объектов или словарь по id).
- [ ] Команды: список, добавить, выдать, вернуть, поиск, статистика.
- [ ] **Исключения** для ошибок (книга не найдена, уже выдана) — свои классы.
- [ ] **Сохранение/загрузка в JSON** (книги переживают перезапуск).
- [ ] Проект разбит минимум на 2 модуля (`library.py` + `main.py`).
- [ ] Корректная обработка кривого ввода (не падает).

---

## 🪜 Пошаговый план

1. **Класс Book.** Атрибуты: id, title, author, year, доступна/у кого. `__repr__` для печати.
2. **Класс Library.** Хранит книги, методы `add`, `find`, `lend`, `return_book`, `all`,
   `stats`.
3. **Исключения.** `BookNotFound`, `BookAlreadyLent` — свои классы.
4. **Меню.** Цикл команд в `main.py`, вызовы методов библиотеки, обработка исключений.
5. **JSON.** `save_to_json` / `load_from_json` — сериализация книг (помни про `__dict__`
   или `dataclasses.asdict`).
6. **Модули.** `library.py` (Book, Library, исключения) + `main.py` (интерфейс).

---

## 🧱 Скелет

**library.py:**
```python
import json
from dataclasses import dataclass, asdict, field

class BookNotFound(Exception):
    pass

class BookAlreadyLent(Exception):
    pass

@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int
    borrowed_by: str | None = None

    def is_available(self) -> bool:
        return self.borrowed_by is None

class Library:
    def __init__(self):
        self.books: dict[int, Book] = {}
        self._next_id = 1

    def add(self, title, author, year):
        book = Book(self._next_id, title, author, year)
        self.books[book.id] = book
        self._next_id += 1
        return book

    def lend(self, book_id, reader):
        book = self.books.get(book_id)
        if book is None:
            raise BookNotFound(f"Нет книги с id={book_id}")
        if not book.is_available():
            raise BookAlreadyLent(f"Книга уже у {book.borrowed_by}")
        book.borrowed_by = reader

    # реализуй return_book, find, stats сам!

    def save(self, filename):
        data = {"next_id": self._next_id,
                "books": [asdict(b) for b in self.books.values()]}
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self, filename):
        try:
            with open(filename, encoding="utf-8") as f:
                data = json.load(f)
            self._next_id = data["next_id"]
            self.books = {b["id"]: Book(**b) for b in data["books"]}
        except FileNotFoundError:
            pass        # первый запуск — файла ещё нет
```

**main.py** — меню, чтение команд, вызовы с `try/except`.

---

## 💪 Усложнения (для «отлично»)

- ➕ Поиск по автору/году/части названия (фильтры).
- ➕ Сортировка списка по разным полям.
- ➕ Читатели как отдельный класс, история выдач.
- ➕ Статистика: сколько выдано, топ авторов (Counter).
- ➕ Импорт каталога из CSV.
- ➕ Юнит-тесты для методов `Library` (модуль `unittest` или `pytest`).
- ➕ Цветной вывод в консоль.

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | ООП + все команды + JSON-сохранение + свои исключения + модули |
| 🌟 Хорошо | + поиск/фильтры/сортировка, статистика |
| 🏆 Отлично | + тесты ИЛИ CSV-импорт ИЛИ читатели с историей, аккуратная обработка ошибок |

Сохрани в `my-code/Python/03-library/`. 🎉

➡️ Финальный рывок: [Уровень 4 · Senior](../04-senior/20-memory-deep.md)
