# ✅ Задачи · Уровень 4 (Senior Rust)

> Сложность: ⭐ средне · ⭐⭐ сложно · ⭐⭐⭐ челлендж. Замеры — только в `--release`.

---

## 🟢 Блок A — умные указатели

1. ⭐ **Box** + рекурсивный список.
2. ⭐⭐ **Rc** + strong_count в разных точках.
3. ⭐⭐ **RefCell** + паника двойного заимствования.
4. ⭐⭐⭐ **Rc<RefCell>** дерево/граф.
5. ⭐⭐⭐ **Weak** — родитель↔ребёнок без утечки.

---

## 🟢 Блок B — многопоточность

6. ⭐ **Поток** + join.
7. ⭐ **move** в поток.
8. ⭐⭐ **Попытка гонки** → ошибка компиляции (объясни).
9. ⭐⭐ **Arc<Mutex>** счётчик из 10 потоков.
10. ⭐⭐⭐ **Параллельная сумма** массива по частям.
11. ⭐⭐⭐ **Каналы** producer-consumer.

---

## 🟢 Блок C — трейты

12. ⭐⭐ **Box<dyn Trait>** — разные типы в Vec.
13. ⭐⭐ **Свой Iterator** + использование map/sum.
14. ⭐⭐ **Add** для Vector2D.
15. ⭐⭐⭐ **Система команд** на трейт-объектах.

---

## 🟢 Блок D — unsafe/FFI

16. ⭐⭐ **Сырые указатели** в unsafe.
17. ⭐⭐⭐ **FFI** — вызов C-функции из libc.

---

## 🟢 Блок E — производительность

18. ⭐ **debug vs release** замер.
19. ⭐⭐ **Итератор vs цикл** (zero-cost).
20. ⭐⭐⭐ **flamegraph** — найди узкое место.

---

## 🟢 Блок F — качество

21. ⭐ **Тесты** (#[test], should_panic).
22. ⭐⭐ **clippy + fmt + doc** на проекте.
23. ⭐⭐⭐ **async** база с tokio.

---

## 🧩 Куда расти

- [The Rust Book](https://doc.rust-lang.org/book/) — дочитать до конца.
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/), [Rustlings](https://github.com/rust-lang/rustlings).
- [Too Many Linked Lists](https://rust-unofficial.github.io/too-many-lists/) — владение через списки (легендарный туториал).
- [Build Your Own X](https://github.com/codecrafters-io/build-your-own-x) — свой веб-сервер, БД, интерпретатор на Rust.
- Направления: веб (axum/actix), CLI (clap), embedded, async (tokio), WebAssembly.

---

## 🏁 Критерий «Senior-зачёт»

- Блок A — Rc + RefCell + (Weak ИЛИ дерево).
- Блок B — Arc<Mutex> + гонка-как-ошибка + (каналы ИЛИ параллельная сумма).
- Блок C — dyn + свой Iterator.
- Блоки D, E, F — минимум по одной (F — тесты обязательно).

➡️ [🚀 Финальные пет-проекты](PROJECT.md)
