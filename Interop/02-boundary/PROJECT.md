# 🚀 Пет-проект уровня 2 — Безопасная Python-обёртка над C-библиотекой

> 🎯 **Цель:** взять C-библиотеку с ресурсами (память, структуры, строки) и построить
> **полностью безопасную** Python-обёртку: пользователь работает с обычными Python-объектами
> и не знает про указатели, владение и `\0`. Это эталон правильной интеграции.

---

## 📋 Что делаем

Выбираешь предметную область со «структурами и ресурсами» и реализуешь её ядро на C, а
сверху — безопасный Python-API. Идеи:
- **динамический буфер/строка** (как StrBuf из [C-проекта](../../C/03b-projects-api/PROJECT.md));
- **стек/очередь/список** с opaque handle;
- **простая «база» ключ-значение** в памяти;
- **обработчик данных** (структуры записей + операции).

---

## ✅ Требования (минимум)

- [ ] C-библиотека с **opaque handle** (`*_new` / `*_free`) — внутренности скрыты.
- [ ] Операции, работающие со структурами и/или строками через границу.
- [ ] Python-класс-обёртка, **связывающий C-ресурс с объектом** (`__del__` + `with`).
- [ ] **Вызывающий-владеет** для буферов где возможно; парные make/free где нет.
- [ ] Все строки — корректно (UTF-8, encode/decode).
- [ ] Структуры — согласованная раскладка (сверка sizeof).
- [ ] Точные сигнатуры, проверка NULL/кодов ошибок → исключения Python.
- [ ] C-часть протестирована **под ASan**; обёртка — без утечек.
- [ ] Пользователь обёртки **ни разу не пишет ctypes** — только чистый Python.

---

## 🪜 Пошаговый план

1. **Спроектируй C-API** с opaque handle (модуль 09): `thing_new`, операции, `thing_free`.
2. **Реализуй C**, протестируй отдельной C-программой под ASan.
3. **FFI-слой** (тонкий, модуль 12): объяви все сигнатуры в одном месте.
4. **Обёртка-класс**: конструктор зовёт `*_new`, `__del__`/`__exit__` зовёт `*_free`.
5. **Безопасные методы**: проверки, перевод C-ошибок в исключения, encode/decode строк.
6. **Тесты**: создание/уничтожение, операции, краевые случаи; проверь отсутствие утечек.

---

## 🧱 Скелет

`store.c`:
```c
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

struct Store {            // opaque — наружу не видно
    char** items;
    int32_t count;
    int32_t capacity;
};

struct Store* store_new(void) {
    struct Store* s = calloc(1, sizeof(struct Store));
    return s;
}

int32_t store_add(struct Store* s, const char* item) {
    // realloc при необходимости, strdup(item)... (реализуй)
    return 0;  // 0 = успех
}

int32_t store_count(const struct Store* s) { return s ? s->count : -1; }

void store_free(struct Store* s) {
    if (!s) return;
    for (int32_t i = 0; i < s->count; i++) free(s->items[i]);
    free(s->items);
    free(s);
}
```
```bash
gcc -shared -fPIC -O2 store.c -o store.so
# и отдельный тест: gcc -fsanitize=address -g test.c store.c -o test && ./test
```

`store.py`:
```python
import ctypes

_lib = ctypes.CDLL("./store.so")
_lib.store_new.restype = ctypes.c_void_p
_lib.store_add.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
_lib.store_add.restype = ctypes.c_int32
_lib.store_count.argtypes = [ctypes.c_void_p]
_lib.store_count.restype = ctypes.c_int32
_lib.store_free.argtypes = [ctypes.c_void_p]

class Store:
    """Безопасное хранилище строк поверх C. Без ctypes наружу."""
    def __init__(self):
        self._h = _lib.store_new()
        if not self._h:
            raise MemoryError("не удалось создать Store")

    def add(self, item: str) -> None:
        code = _lib.store_add(self._h, item.encode("utf-8"))
        if code != 0:
            raise RuntimeError(f"store_add failed: {code}")

    def __len__(self) -> int:
        return _lib.store_count(self._h)

    def close(self):
        if self._h:
            _lib.store_free(self._h)
            self._h = None

    def __del__(self): self.close()
    def __enter__(self): return self
    def __exit__(self, *a): self.close()

# использование — чистый Python, ноль ctypes:
with Store() as s:
    s.add("привет")
    s.add("мир")
    print(len(s))   # 2
```

---

## 💪 Усложнения (для «отлично»)

- ➕ Метод получения элемента (строка из C через буфер вызывающего).
- ➕ Поддержка `numpy`/`bytes` без копирования для бинарных данных.
- ➕ Полный набор операций (удаление, поиск, итерация через `__iter__`).
- ➕ Юнит-тесты (`pytest`), проверка отсутствия утечек.
- ➕ Версия ядра на **Rust** вместо C (превью Уровня 3) — сравни безопасность.
- ➕ Оформи как устанавливаемый пакет.

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | opaque handle, RAII-обёртка, безопасные методы, ASan чист, ноль ctypes наружу |
| 🌟 Хорошо | + полный набор операций, тесты, работа со строками через буфер |
| 🏆 Отлично | + numpy/bytes без копий ИЛИ Rust-ядро, пакет, аккуратная документация владения |

---

## 🎓 Чему ты научился

Ты построил то, как устроены **все** хорошие нативные библиотеки Python: безопасный,
питоничный фасад над опасным нативным ядром, с правильным управлением памятью на границе.
Это вершина темы памяти всего курса — управление ею **между** языками.

➡️ Дальше — [Уровень 3 · Конкретные связки](../03-bindings/13-c-rust.md)
