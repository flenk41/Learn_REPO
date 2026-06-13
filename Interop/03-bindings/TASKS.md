# ✅ Задачи · Уровень 3 (конкретные связки)

> Выбирай связки под свои языки из курса. Сложность: ⭐ · ⭐⭐ · ⭐⭐⭐

---

## 🟢 Блок A — C + Rust

1. ⭐⭐ **Rust зовёт C** (libc abs/sqrt).
2. ⭐⭐ **Rust для C** — cdylib + вызов из Python.
3. ⭐⭐ **CString / #[repr(C)]** — строки и структуры.
4. ⭐⭐⭐ **bindgen** — автогенерация биндингов.

---

## 🟢 Блок B — Rust + Python (PyO3)

5. ⭐⭐ **Первый модуль** PyO3 + maturin.
6. ⭐⭐ **Замер** Python vs Rust+PyO3.
7. ⭐⭐ **#[pyclass]** — Rust-структура как Python-класс.
8. ⭐⭐⭐ **Сравнение** ctypes+C vs PyO3+Rust.

---

## 🟢 Блок C — Python + JS

9. ⭐⭐ **REST-связка** Python ↔ JS.
10. ⭐⭐ **Подпроцесс** Python → Node (JSON).
11. ⭐⭐⭐ **Pyodide** — Python в браузере.

---

## 🟢 Блок D — WebAssembly

12. ⭐⭐ **Rust → WASM** + вызов из JS.
13. ⭐⭐ **Замер** JS vs WASM.
14. ⭐⭐⭐ **C → WASM** (Emscripten).

---

## 🟢 Блок E — встраивание и клей

15. ⭐⭐ **Встрой Python** в C.
16. ⭐⭐ **Скрипт из файла** (настраиваемое приложение).
17. ⭐⭐ **REST между сервисами** на разных языках.
18. ⭐⭐⭐ **FFI vs REST** — сравнение одной задачи.

---

## 🧩 Где тренироваться

- [PyO3](https://pyo3.rs) / [maturin](https://www.maturin.rs) — Rust+Python.
- [wasm-bindgen](https://rustwasm.github.io/wasm-bindgen/) / [Emscripten](https://emscripten.org).
- [bindgen](https://rust-lang.github.io/rust-bindgen/) / [cbindgen](https://github.com/mozilla/cbindgen).
- [gRPC](https://grpc.io) / [FastAPI](https://fastapi.tiangolo.com) для REST.

---

## 🏁 Критерий «зачёт»

- Минимум **2 разные связки** доведены до рабочего примера (например Rust+Python и REST).
- Минимум 1 из блоков A/B (тесная связь через биндинги).
- Минимум 1 из блоков C/E (свободная связь).

➡️ [🚀 Полиглотное приложение](PROJECT.md)
