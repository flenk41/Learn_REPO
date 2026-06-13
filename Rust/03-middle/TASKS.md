# ✅ Задачи · Уровень 3 (Middle Rust)

> Проверяй через `cargo clippy` (линтер) и `cargo test`. Сложность: ⭐ · ⭐⭐ · ⭐⭐⭐

---

## 🟢 Блок A — структуры

1. ⭐ **Rectangle** с методами и `new`.
2. ⭐⭐ **Point** с derive(Debug, Clone, PartialEq) + расстояние.
3. ⭐⭐ **BankAccount** (deposit/withdraw/balance).
4. ⭐⭐ **newtype** Celsius/Fahrenheit с переводом.

---

## 🟢 Блок B — enum и Option

5. ⭐ **TrafficLight** + следующий сигнал через match.
6. ⭐⭐ **Shape enum** с площадью через match.
7. ⭐⭐ **Безопасное деление** → Option.
8. ⭐⭐ **Поиск** → Option<usize>.

---

## 🟢 Блок C — обработка ошибок

9. ⭐⭐ **divide** → Result.
10. ⭐⭐ **parse через ?** → Result.
11. ⭐⭐⭐ **Цепочка `?`** — чтение+парсинг+вычисление.

---

## 🟢 Блок D — обобщения и трейты

12. ⭐⭐ **largest<T>** для любого сравнимого.
13. ⭐⭐ **Трейт Shape** для Circle/Rectangle.
14. ⭐⭐ **Display** для своей структуры.
15. ⭐⭐⭐ **Обобщённый Stack<T>** с trait bound.

---

## 🟢 Блок E — коллекции

16. ⭐ **Vec** — сумма/min/max/удвоение.
17. ⭐⭐ **Частота слов** (HashMap + entry).
18. ⭐⭐ **Уникальные** (HashSet).
19. ⭐⭐ **Телефонная книга** (HashMap).
20. ⭐⭐⭐ **Топ-N слов**.

---

## 🟢 Блок F — замыкания и итераторы

21. ⭐ **map/filter/collect**.
22. ⭐⭐ **Конвейер** обработки текста.
23. ⭐⭐ **fold** — произведение/свёртка.
24. ⭐⭐⭐ **Среднее и медиана** через итераторы.

---

## 🧩 Где тренироваться

- [Rustlings](https://github.com/rust-lang/rustlings) — разделы structs, enums, error_handling, generics, traits, iterators.
- [The Rust Book](https://doc.rust-lang.org/book/) — главы 5–13.
- [Exercism — Rust](https://exercism.org/tracks/rust).

---

## 🏁 Критерий «зачёт»

- Блоки A, B — минимум по 3.
- Блок C — минимум 2 (включая `?`).
- Блок D — минимум 2 (включая трейт).
- Блоки E, F — минимум по 2.

➡️ [🚀 CLI-приложение](PROJECT.md)
