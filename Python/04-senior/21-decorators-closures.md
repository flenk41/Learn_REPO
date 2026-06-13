# 21 · Декораторы и замыкания 🖼️

> 🎯 **Цель блока:** понять замыкания (как функции «помнят» переменные в памяти) и
> декораторы — мощный инструмент, который ты постоянно видишь (`@dataclass`, `@property`).

---

## 📖 Функции — это объекты

В Python функция — обычный объект (вспомни Уровень 2: всё — объект). Её можно передавать,
возвращать, присваивать:

```python
def greet(name):
    return f"Привет, {name}"

f = greet              # присвоить (ярлык на тот же объект-функцию)
print(f("Гена"))       # Привет, Гена

def apply(func, value):
    return func(value) # передать функцию как аргумент
print(apply(greet, "Кот"))
```

---

## ⭐ Замыкание (closure) — функция помнит окружение

Внутренняя функция «запоминает» переменные внешней — даже после того, как внешняя
завершилась. Эти переменные продолжают жить в памяти.

```python
def make_multiplier(factor):
    def multiply(x):
        return x * factor      # factor "захвачен" из внешней функции
    return multiply            # возвращаем внутреннюю функцию

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5))               # 10  — помнит factor=2
print(triple(5))               # 15  — помнит factor=3
```

🖼️ Что в памяти:

```
   double ──► [функция multiply + захваченное окружение {factor: 2}]
   triple ──► [функция multiply + захваченное окружение {factor: 3}]

   Каждое замыкание держит СВОЮ копию окружения живой в памяти.
```

> 💡 Замыкание — это функция + «рюкзачок» с переменными, которые она унесла с собой.
> Посмотреть захваченное: `double.__closure__[0].cell_contents` → 2.

---

## ⭐ Декоратор — функция, оборачивающая функцию

Декоратор принимает функцию и возвращает **новую** функцию с добавленным поведением.

```python
def logged(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__} с {args}")
        result = func(*args, **kwargs)
        print(f"→ результат {result}")
        return result
    return wrapper

@logged                    # это то же, что add = logged(add)
def add(a, b):
    return a + b

add(2, 3)
# Вызов add с (2, 3)
# → результат 5
```

🖼️ Что делает `@logged`:

```
   @logged
   def add(...): ...     ≡     add = logged(add)

   add теперь указывает на wrapper, который ВНУТРИ зовёт оригинальный add
```

> 💡 `*args, **kwargs` в обёртке позволяют декоратору работать с **любой** функцией.

### Сохраняй метаданные через functools.wraps

```python
from functools import wraps

def logged(func):
    @wraps(func)               # сохранить имя/докстринг оригинала
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
```

---

## 📖 Практичные декораторы

### Замер времени
```python
import time
from functools import wraps

def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter()-start:.4f} сек")
        return result
    return wrapper

@timed
def slow():
    return sum(range(10_000_000))
```

### Кэширование (мемоизация) — встроенный декоратор!
```python
from functools import lru_cache

@lru_cache(maxsize=None)       # запоминает результаты в памяти
def fib(n):
    if n < 2:
        return n
    return fib(n-1) + fib(n-2)

print(fib(100))                # мгновенно! без кэша — вечность
```

💡 `lru_cache` хранит результаты в словаре (память в обмен на скорость). Прямая связь
тем: кэш = структура в памяти.

---

## 📖 Декоратор с аргументами

```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def hello():
    print("привет")

hello()        # печатает "привет" 3 раза
```

---

## 📖 @property — метод как атрибут

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):                # вызывается как атрибут, без ()
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)                      # 78.5  (не c.area()!)
```

---

## ✅ Задачи

1. **Замыкание-счётчик.** Функция `make_counter()`, возвращающая функцию, которая при
   каждом вызове увеличивает и возвращает счётчик. Сделай два независимых счётчика.
2. **Замыкание-аккумулятор.** `make_accumulator()` — суммирует все переданные ему числа.
3. **Декоратор @timed.** Замерь время выполнения функции.
4. **Декоратор @logged** с `functools.wraps`.
5. **lru_cache.** Сравни время `fib(35)` с кэшем и без.
6. **Декоратор с аргументом @repeat(n).**
7. **@property.** Класс «Температура» с `@property` для перевода C↔F.
8. ⭐ **Декоратор-валидатор:** проверяет, что аргументы функции положительны, иначе
   бросает исключение.

---

## ❓ Проверь себя

1. Что значит «функция — объект первого класса»?
2. Что такое замыкание? Что оно «захватывает» и где это живёт?
3. Что делает декоратор? Как `@dec` разворачивается?
4. Зачем `*args, **kwargs` в обёртке?
5. Зачем `functools.wraps`?
6. Что делает `lru_cache` и какой ценой?

---

## ✅ Чек-лист

- [ ] Понимаю функции как объекты
- [ ] Понимаю замыкания и захват окружения в памяти
- [ ] Пишу декораторы (в т.ч. с аргументами)
- [ ] Использую `functools.wraps` и `lru_cache`
- [ ] Применяю `@property`

➡️ Следующий: [22 · Профилирование](22-profiling.md)
