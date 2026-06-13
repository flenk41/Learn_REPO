# 13 · Структуры и методы

> 🎯 **Цель блока:** научиться создавать свои типы через `struct` и добавлять им поведение
> через `impl`. Здесь закрепляется работа с `&self` из Уровня 2.

---

## 📖 Структуры

```rust
struct User {
    name: String,
    age: u32,
    active: bool,
}

let user = User {
    name: String::from("Гена"),
    age: 30,
    active: true,
};

println!("{} — {} лет", user.name, user.age);
```

Изменяемая структура:
```rust
let mut user = User { name: String::from("Гена"), age: 30, active: true };
user.age = 31;            // вся структура должна быть mut
```

> ⚠️ `mut` относится ко **всей** структуре — нельзя сделать изменяемым только одно поле.

---

## 📖 Сокращения и обновление

```rust
fn build(name: String, age: u32) -> User {
    User {
        name,            // сокращение: name вместо name: name
        age,
        active: true,
    }
}

// создать на основе другой структуры
let user2 = User {
    name: String::from("Чебур"),
    ..user               // остальные поля взять из user
};
```

---

## ⭐ Методы через `impl`

```rust
struct Rectangle {
    width: f64,
    height: f64,
}

impl Rectangle {
    // метод — первый параметр &self
    fn area(&self) -> f64 {
        self.width * self.height
    }

    fn perimeter(&self) -> f64 {
        2.0 * (self.width + self.height)
    }

    // &mut self — метод, меняющий структуру
    fn scale(&mut self, factor: f64) {
        self.width *= factor;
        self.height *= factor;
    }

    // ассоциированная функция (без self) — часто конструктор
    fn new(width: f64, height: f64) -> Self {
        Rectangle { width, height }
    }

    fn square(size: f64) -> Self {
        Rectangle { width: size, height: size }
    }
}

let mut rect = Rectangle::new(3.0, 4.0);   // вызов через ::
println!("{}", rect.area());               // 12 — вызов через .
rect.scale(2.0);
let sq = Rectangle::square(5.0);
```

🖼️ Разбор `self`:
```
   fn area(&self)        — заимствует структуру для чтения (как &)
   fn scale(&mut self)   — заимствует для изменения (как &mut)
   fn new(...)           — без self → ассоциированная функция (вызов Type::new)
   fn consume(self)      — забирает владение структурой
```

💡 Это прямое продолжение Уровня 2: `&self` = читаем, `&mut self` = меняем, `self` =
забираем владение. Методы вызываются через `.`, ассоциированные функции — через `::`.

---

## 📖 Производные трейты (derive)

`#[derive(...)]` автоматически добавляет полезное поведение:

```rust
#[derive(Debug, Clone, PartialEq)]
struct Point {
    x: i32,
    y: i32,
}

let p = Point { x: 1, y: 2 };
println!("{:?}", p);          // Point { x: 1, y: 2 } — благодаря Debug
let p2 = p.clone();           // благодаря Clone
println!("{}", p == p2);      // true — благодаря PartialEq
```

| derive | Что даёт |
|--------|----------|
| `Debug` | печать через `{:?}` |
| `Clone` | метод `.clone()` |
| `Copy` | копирование вместо move (для маленьких) |
| `PartialEq` | сравнение `==` |
| `Default` | значение по умолчанию |

💡 `#[derive(Debug)]` + `{:?}` — твой главный инструмент отладки. Добавляй `Debug` ко всем
структурам.

---

## 📖 Кортежные структуры и юнит-структуры

```rust
struct Color(u8, u8, u8);          // кортежная структура (поля без имён)
let red = Color(255, 0, 0);
println!("{}", red.0);             // доступ по индексу

struct Meters(f64);                // newtype — обёртка для типобезопасности
let distance = Meters(100.0);
```

💡 `Meters(f64)` — приём «newtype»: оборачивает тип, чтобы не перепутать метры с
килограммами. Компилятор не даст смешать `Meters` и `Kilograms`.

---

## ✅ Задачи

1. **Rectangle** с методами площади, периметра, `scale` (`&mut self`), `new`/`square`.
2. **Point** с `#[derive(Debug, Clone, PartialEq)]`, метод расстояния до другой точки.
3. **BankAccount** — структура со счётом, методы `deposit`/`withdraw` (с проверкой)/`balance`.
4. **Circle** с `area`, `new`. Сравни площади двух кругов.
5. **newtype.** Создай `Celsius(f64)` и `Fahrenheit(f64)`, метод перевода между ними.
6. ⭐ **Counter** — структура-счётчик с `&mut self`-методом `increment` и `&self`-методом `get`.

---

## ❓ Проверь себя

1. Как объявить и создать структуру?
2. Чем `&self`, `&mut self`, `self` в методах отличаются?
3. Чем метод отличается от ассоциированной функции? Как каждую вызвать?
4. Что делает `#[derive(Debug)]`?
5. Что такое кортежная структура и newtype?

---

## ✅ Чек-лист

- [ ] Создаю структуры, понимаю `mut` для всей структуры
- [ ] Пишу методы с правильным `self`
- [ ] Использую ассоциированные функции (конструкторы)
- [ ] Применяю `#[derive(Debug, Clone, PartialEq)]`
- [ ] Знаю про newtype для типобезопасности

➡️ Следующий: [14 · Перечисления и Option](14-enums-option.md)
