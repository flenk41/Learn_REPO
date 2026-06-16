# 🚀 Мини-проект · Библиотека фигур (shapes)

> Спроектируй маленькую **ООП-библиотеку** для работы с геометрическими фигурами. Цель —
> применить всё: абстракцию, инкапсуляцию, полиморфизм, свойства и магические методы вместе.

---

## 🎯 Что делаем

Пакет `shapes/`, который умеет создавать фигуры, считать их площадь/периметр, сравнивать,
сортировать и складывать в «холст».

```
shapes/
├── __init__.py        # публичный API: что видно снаружи
├── base.py            # абстрактный Shape (ABC)
├── figures.py         # Circle, Rectangle, Square, Triangle
└── canvas.py          # Canvas — контейнер фигур
```

---

## 📋 Требования

### 1. Абстрактный базовый класс (`base.py`)

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float: ...
    @abstractmethod
    def perimeter(self) -> float: ...

    def __repr__(self):                 # общий для всех
        return f"{type(self).__name__}(area={self.area():.2f})"
    def __eq__(self, other):            # равны по площади
        return isinstance(other, Shape) and abs(self.area() - other.area()) < 1e-9
    def __lt__(self, other):            # сравнение по площади → сортировка
        return self.area() < other.area()
```

- ✅ Нельзя создать `Shape()` напрямую.
- ✅ Каждая фигура **обязана** реализовать `area()` и `perimeter()`.

### 2. Конкретные фигуры (`figures.py`)

- `Circle(radius)`, `Rectangle(width, height)`, `Square(side)`, `Triangle(a, b, c)`.
- Размеры — через `@property` с **проверкой** (> 0), иначе `ValueError`.
- `Square` — подумай: наследовать от `Rectangle` или нет? (см. подсказку ниже про LSP).
- `area()`/`perimeter()` у каждой свои — это **полиморфизм**.

### 3. Холст-контейнер (`canvas.py`)

```python
class Canvas:
    def __init__(self): self._shapes = []
    def add(self, shape): ...           # принимает любой Shape
    def total_area(self): ...           # сумма площадей (полиморфно, без isinstance)
    def __len__(self): ...              # len(canvas)
    def __iter__(self): ...             # for shape in canvas
    def __getitem__(self, i): ...       # canvas[0]
```

### 4. Демо (`main.py` или `__main__`)

```python
canvas = Canvas()
canvas.add(Circle(2))
canvas.add(Rectangle(3, 4))
canvas.add(Square(5))

print(f"Фигур: {len(canvas)}")
print(f"Суммарная площадь: {canvas.total_area():.2f}")
print("По возрастанию площади:", sorted(canvas))     # работает благодаря __lt__
biggest = max(canvas)                                 # благодаря __lt__
print("Самая большая:", biggest)
```

---

## 🌟 Бонусы (по желанию)

- 🥚 **Protocol вместо ABC.** Сделай вариант, где `Canvas.add` принимает `Drawable` Protocol.
- 🐣 **Контекст-менеджер.** `with canvas.batch():` — группировка добавлений с печатью итога на выходе.
- 🐥 **Сериализация-миксин.** `JsonMixin` для экспорта фигуры в JSON (`to_json`).
- 🦅 **@total_ordering** на `Shape`, чтобы получить все сравнения из `__eq__` и `__lt__`.
- 🚀 **Тесты.** Покрой `pytest`: создание, проверки (>0), площади, сортировку, запрет `Shape()`.

---

## 💡 Подсказки по проектированию

- **Square vs Rectangle.** Классический спор: «квадрат — это прямоугольник?». С точки зрения
  геометрии да, но если `Rectangle` имеет независимые сеттеры `width`/`height`, то `Square`-
  наследник **нарушит** ожидания (LSP). Часто чище — общий предок или композиция. Это прямо
  иллюстрирует [принцип подстановки Лисков (LSP)](../../OOP/03-design/15-lsp-isp-dip.md).
- **Инкапсуляция.** Храни размеры в `_field`, отдавай через `@property` с валидацией.
- **Полиморфизм.** `total_area` не должна знать конкретные классы — только метод `area()`.

> 🏛️ Этот проект — мост к треку **ООП**: ты применяешь [четыре столпа](../../OOP/02-pillars/08-abstraction.md)
> и упираешься в [SOLID](../../OOP/03-design/13-solid-intro.md) на живом примере.

---

## ✅ Критерии готовности

- [ ] `Shape` — `ABC`, создать нельзя; наследники реализуют `area`/`perimeter`
- [ ] Размеры инкапсулированы через `@property` с проверкой > 0
- [ ] `total_area` полиморфна (без `isinstance`)
- [ ] `Canvas` ведёт себя как коллекция (`len`, `for`, `[]`)
- [ ] Фигуры сравниваются и сортируются по площади
- [ ] Осознанно решён вопрос `Square`/`Rectangle` (LSP)

🎉 Готово? Ты владеешь ООП на Python и готов к [Уровню 4 · Senior](../README.md).
