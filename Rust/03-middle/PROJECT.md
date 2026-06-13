# 🚀 Пет-проект уровня 3 — Менеджер задач (CLI)

> 🎯 **Цель:** собрать всё из Middle — структуры, enum, Result, обобщения, коллекции,
> итераторы — в консольное приложение с сохранением. Это «портфолио-проект» на Rust.

---

## 📋 Что должна уметь программа

Менеджер задач, запоминающий задачи между запусками (JSON-файл):

```
==== ЗАДАЧИ ====
[1] [ ] Купить хлеб           (приоритет: 2)
[2] [x] Сделать домашку       (приоритет: 1)
[3] [ ] Позвонить маме        (приоритет: 3)

Команды: add / done <id> / delete <id> / list / quit
> add Помыть посуду 2
Задача добавлена (id=4)
> done 1
Задача 1 выполнена
> quit
Сохранено. Пока!
```

---

## ✅ Требования (минимум)

- [ ] Структура `Task` (id, title, done, priority) с `#[derive(...)]`.
- [ ] Хранение в `Vec<Task>`.
- [ ] enum `Command` для разбора команд (по желанию).
- [ ] Команды: add, done, delete, list, quit.
- [ ] Обработка ошибок через `Result`/`Option` (нет задачи с id, кривой ввод — не падать).
- [ ] **Сохранение/загрузка в JSON** (библиотека `serde` + `serde_json`).
- [ ] Использование итераторов (фильтрация, поиск, сортировка).
- [ ] Чисто по `cargo clippy`.

---

## 🪜 Пошаговый план

1. **Проект.** `cargo new task_manager`. Добавь зависимости в `Cargo.toml`:
   ```toml
   serde = { version = "1", features = ["derive"] }
   serde_json = "1"
   ```
2. **Структура.** `Task` с `#[derive(Serialize, Deserialize, Debug, Clone)]`.
3. **Хранилище.** `Vec<Task>` + счётчик id.
4. **Команды.** Цикл чтения, разбор строки (`split`), `match` по команде.
5. **add/done/delete.** Найди задачу через итераторы (`iter().find()` / `position()`).
6. **list.** Печать с галочками, возможно сортировка по приоритету (итератор + `sort_by`).
7. **JSON.** `serde_json::to_string` / `from_str`, чтение/запись файла.
8. **Полировка.** clippy, обработка ошибок.

---

## 🧱 Скелет

```rust
use serde::{Serialize, Deserialize};
use std::fs;

#[derive(Serialize, Deserialize, Debug, Clone)]
struct Task {
    id: u32,
    title: String,
    done: bool,
    priority: u8,
}

struct TaskManager {
    tasks: Vec<Task>,
    next_id: u32,
}

impl TaskManager {
    fn new() -> Self {
        TaskManager { tasks: Vec::new(), next_id: 1 }
    }

    fn add(&mut self, title: String, priority: u8) {
        self.tasks.push(Task {
            id: self.next_id, title, done: false, priority,
        });
        self.next_id += 1;
    }

    fn done(&mut self, id: u32) -> Result<(), String> {
        match self.tasks.iter_mut().find(|t| t.id == id) {
            Some(task) => { task.done = true; Ok(()) }
            None => Err(format!("Нет задачи с id={}", id)),
        }
    }

    fn list(&self) {
        for t in &self.tasks {
            let mark = if t.done { "x" } else { " " };
            println!("[{}] [{}] {} (приоритет: {})", t.id, mark, t.title, t.priority);
        }
    }

    fn save(&self, path: &str) -> Result<(), Box<dyn std::error::Error>> {
        let json = serde_json::to_string_pretty(&self.tasks)?;
        fs::write(path, json)?;
        Ok(())
    }

    fn load(path: &str) -> Self {
        match fs::read_to_string(path) {
            Ok(data) => {
                let tasks: Vec<Task> = serde_json::from_str(&data).unwrap_or_default();
                let next_id = tasks.iter().map(|t| t.id).max().unwrap_or(0) + 1;
                TaskManager { tasks, next_id }
            }
            Err(_) => TaskManager::new(),   // первый запуск
        }
    }
    // реализуй delete сам
}

fn main() {
    let mut mgr = TaskManager::load("tasks.json");
    // цикл чтения команд...
    mgr.save("tasks.json").expect("ошибка сохранения");
}
```

---

## 💪 Усложнения (для «отлично»)

- ➕ Сортировка по приоритету (`sort_by_key`).
- ➕ Фильтры: только невыполненные / по приоритету (итераторы).
- ➕ Статистика: сколько выполнено (через `filter().count()`).
- ➕ Аргументы командной строки (`std::env::args` или библиотека `clap`).
- ➕ Цветной вывод (библиотека `colored`).
- ➕ Тесты (`cargo test`) для методов TaskManager.

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | Все команды + JSON-сохранение + обработка ошибок, clippy чист |
| 🌟 Хорошо | + сортировка/фильтры/статистика |
| 🏆 Отлично | + clap или тесты, цветной вывод, идиоматичный код |

---

## 🎓 Чему ты научился

Ты собрал настоящее приложение с персистентностью, использовав структуры, `Result`,
коллекции, итераторы и популярную библиотеку `serde`. И всё это — без единой ошибки памяти,
гарантированно, благодаря владению.

➡️ Финальный рывок: [Уровень 4 · Senior](../04-senior/19-smart-pointers.md)
