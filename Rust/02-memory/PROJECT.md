# 🚀 Пет-проект уровня 2 — Свой динамический стек

> 🎯 **Цель:** реализовать структуру данных «стек» на базе `Vec`, прочувствовав владение,
> заимствование и методы с `&self`/`&mut self`. Это закрепит ядро Rust на практике.

> 💡 В отличие от C/C++, тут ты **не управляешь памятью вручную** — `Vec` делает это, а ты
> учишься правильно раздавать владение и ссылки через API.

---

## 📋 Что делаем

Обобщённый стек `Stack<T>` (LIFO) с безопасным API:

```rust
let mut s: Stack<i32> = Stack::new();
s.push(1);
s.push(2);
s.push(3);
println!("{:?}", s.peek());   // Some(3) — заглянуть, не забирая
println!("{:?}", s.pop());    // Some(3) — снять с вершины
println!("{}", s.len());      // 2
```

---

## ✅ Требования (минимум)

- [ ] Обобщённая структура `Stack<T>` на базе `Vec<T>`.
- [ ] Методы: `new`, `push`, `pop` (→ `Option<T>`), `peek` (→ `Option<&T>`), `len`,
      `is_empty`.
- [ ] Правильное использование `&self` (чтение) и `&mut self` (изменение).
- [ ] `pop` возвращает `Option<T>` (владение), `peek` возвращает `Option<&T>` (ссылку).
- [ ] Компилируется без предупреждений (`cargo clippy`).

---

## 🪜 Пошаговый план

1. **Проект.** `cargo new my_stack --lib` (библиотека) или обычный.
2. **Структура.** `struct Stack<T> { items: Vec<T> }`.
3. **new.** Создаёт пустой стек.
4. **push.** `&mut self`, добавляет в `items`.
5. **pop.** `&mut self`, возвращает `Option<T>` (используй `self.items.pop()`).
6. **peek.** `&self`, возвращает `Option<&T>` (ссылку на вершину, без забирания владения!).
7. **len/is_empty.** `&self`.
8. **Тесты.** Напиши `#[test]`-функции, прогони `cargo test`.

---

## 🧱 Скелет

```rust
pub struct Stack<T> {
    items: Vec<T>,
}

impl<T> Stack<T> {
    pub fn new() -> Self {
        Stack { items: Vec::new() }
    }

    pub fn push(&mut self, value: T) {     // &mut self — меняем стек
        self.items.push(value);
    }

    pub fn pop(&mut self) -> Option<T> {   // отдаём ВЛАДЕНИЕ верхним элементом
        self.items.pop()
    }

    pub fn peek(&self) -> Option<&T> {     // отдаём ССЫЛКУ — стек остаётся владельцем
        self.items.last()
    }

    pub fn len(&self) -> usize {           // &self — только читаем
        self.items.len()
    }

    pub fn is_empty(&self) -> bool {
        self.items.is_empty()
    }
}

fn main() {
    let mut s: Stack<i32> = Stack::new();
    s.push(1);
    s.push(2);
    println!("{:?}", s.peek());   // Some(2)
    println!("{:?}", s.pop());    // Some(2)
    println!("len = {}", s.len());// 1
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_push_pop() {
        let mut s = Stack::new();
        s.push(10);
        s.push(20);
        assert_eq!(s.pop(), Some(20));
        assert_eq!(s.pop(), Some(10));
        assert_eq!(s.pop(), None);
    }
}
```
```powershell
cargo run
cargo test
```

> 💡 Обрати внимание на разницу: `pop` отдаёт `Option<T>` (владение уходит наружу), а
> `peek` отдаёт `Option<&T>` (заимствование — стек остаётся владельцем). Это и есть ядро
> Уровня 2 в действии.

---

## 💪 Усложнения (для «отлично»)

- ➕ Применение: проверка сбалансированности скобок `()[]{}` в строке через стек.
- ➕ `Default`-реализация и `From<Vec<T>>`.
- ➕ Метод `iter()` для перебора (через `&self`).
- ➕ Своя очередь `Queue<T>` по аналогии.
- ➕ Реализация трейта `Display` для красивой печати.
- ➕ Документация (`///`) + `cargo doc`.

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | Все методы, правильные `&self`/`&mut self`, тесты, clippy чист |
| 🌟 Хорошо | + проверка скобок или очередь |
| 🏆 Отлично | + iter, Display, документация |

---

## 🎓 Чему ты научился

Ты построил структуру данных, ни разу не написав ручное управление памятью — `Vec` сделал
это, а ты правильно раздал владение (`pop`) и ссылки (`peek`) через API. Это и есть стиль
Rust: безопасность достаётся бесплатно, если следовать владению.

➡️ Дальше — [Уровень 3 · Middle](../03-middle/13-structs.md)
