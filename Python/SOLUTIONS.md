# ✅ Решебник Python — решения всех задач по категориям

> 🎯 Разборы задач из всех `TASKS.md` трека Python, по уровням. Сначала реши сам — потом сверься.
> Показан **ключевой код** (идея). Инструменты исследования памяти: `id()`, `is`,
> `sys.getrefcount`, `copy`, `sys.getsizeof`, `tracemalloc`.

> 💡 Раскрывай решения по одному (`▶`).

---

## 🐣 Уровень 1 — Основы

<details><summary>Блок A — переменные, числа, строки (1–5)</summary>

**1. Обмен**: `a, b = b, a`. **2. Конвертер**: `print(f"{km*0.621:.2f}")`. **3. Инициалы**: `f, i, o = s.split(); print(f"{f} {i[0]}.{o[0]}.")`. **4. Палиндром**: `s == s[::-1]`. **5. Шифр сдвига**: `"".join(chr(ord(c)+1) for c in s)`.
</details>

<details><summary>Блок B — условия (6–10)</summary>

**6. Время суток**: диапазоны часа (см. решебник C, №6). **7. Тип треугольника**: существование + равенства сторон. **8. Квадратное уравнение**: дискриминант + случаи `a==0`. **9. КНБ**: выигрышные пары. **10. ИМТ**: `bmi = w/(h*h)`, категории по диапазонам (`<18.5` недостаток и т.д.).
</details>

<details><summary>Блок C — циклы (11–17)</summary>

**11. Сумма цифр**: `sum(int(d) for d in str(n))`. **12. FizzBuzz**: `for i in range(1,101): print("FizzBuzz" if i%15==0 else "Fizz" if i%3==0 else "Buzz" if i%5==0 else i)`. **13. НОД**: `while b: a, b = b, a%b`. **14. Фибоначчи**: `a,b=0,1; for _ in range(N): print(a); a,b=b,a+b`. **15. Простые до N**: для каждого `n` проверь делители до `√n`. **16. Шахматная доска**: `(i+j)%2`. **17. Совершенные**: `n == sum(d for d in range(1,n) if n%d==0)`.
</details>

<details><summary>Блок D — функции (18–22)</summary>

**18. max3/min3/average3**: `max(a,b,c)`, `sum((a,b,c))/3`. **19. Калькулятор**: по функции на операцию. **20. Конвертер температур**: `c2f = lambda c: c*9/5+32`. **21. Ханойские башни**: рекурсия (см. решебник C, №18). **22. Ловушка с `lst=[]`**:
```python
def f(x, lst=None):       # НЕ lst=[] — он один на все вызовы (мутабельный дефолт)!
    if lst is None: lst = []
    lst.append(x); return lst
```
</details>

---

## 🐥 Уровень 2 — Память

<details><summary>Блок A — объекты и ссылки (1–4)</summary>

**1. is vs ==**: два одинаковых списка `a==b` True, `a is b` False; алиас `c=a` → `c is a` True. **2. Граница кэша чисел**: малые int (−5..256) кэшированы → `a is b` True; вне диапазона — обычно False. **3. None-детектор**: `if x is None:` (не `==`). **4. Интернирование строк**: короткие литералы-идентификаторы интернируются (`is` True), вычисленные/с пробелами — нет.
</details>

<details><summary>Блок B — изменяемость и алиасинг (5–8)</summary>

**5. Алиасинг-баг**: `b=a; b.append(1)` меняет и `a`; **фикс** `b=a.copy()`. **6. Числа не алиасятся**: int неизменяем → `b=a; b+=1` создаёт новый объект, `a` цел. **7. Кортеж со списком**: `t=([1],); t[0].append(2)` — список внутри менять можно, сам кортеж — нет. **8. Функция-вредитель**: `def bad(l): l.append(0)` портит аргумент; безопасная — `def ok(l): return l+[0]`.
</details>

<details><summary>Блок C — счётчик ссылок и GC (9–11)</summary>

**9. Наблюдение счётчика**: `sys.getrefcount(a)` растёт при `b=a`/добавлении в список, падает при `del`. **10. del**: `del b` убирает **имя**, объект жив, пока есть другие ссылки. **11. Циклическая ссылка**: `a.ref=b; b.ref=a; del a,b` — refcount не дойдёт до 0, освободит сборщик циклов `gc.collect()`.
</details>

<details><summary>Блок D — копирование (12–15)</summary>

**12. Три копии**: алиас (`b=a`) — тот же объект; shallow (`a.copy()`) — новый список, те же вложенные; deep (`copy.deepcopy`) — всё новое. **13. Вложенный баг**: `m2=m.copy()` у матрицы → строки общие; **фикс** `deepcopy`. **14. Словарь со списками**: `copy.deepcopy(d)`. **15. Своя deepcopy** рекурсией:
```python
def my_deepcopy(x):
    return [my_deepcopy(e) for e in x] if isinstance(x, list) else x
```
</details>

<details><summary>Блок E — коллекции (16–21)</summary>

**16. Уникальные слова**: `set(text.split())`. **17. Частота слов**: `collections.Counter(text.split())`. **18. Телефонная книга**: `dict` с add/get/del. **19. Операции над множествами**: `a & b`, `a | b`, `a - b`. **20. Скорость in**: `x in set` — O(1), `x in list` — O(n); замерь `timeit` на 1 млн. **21. Память list vs tuple**: `sys.getsizeof(tuple)` < `list` (кортеж неизменяем, без запаса под рост).
</details>

---

## 🐥 Уровень 3 — Middle

<details><summary>Блок A — словари и множества (1–6)</summary>

**1. Частота символов**: `Counter(s)`. **2. Топ-N слов**: `Counter(words).most_common(n)`. **3. Анаграммы**: ключ `"".join(sorted(word))`, `defaultdict(list)`. **4. Уникальные с порядком**: `list(dict.fromkeys(items))`. **5. Мемоизация**: словарь-кэш `cache[n]=...` или `@lru_cache`. **6. Граф друзей**: словарь смежности, общие — `set(a) & set(b)`.
</details>

<details><summary>Блок B — генераторы (7–11)</summary>

**7. Генератор квадратов**: `(i*i for i in range(N))` — память O(1) vs список O(N) (`getsizeof`). **8. Бесконечный Фибоначчи + islice**: `itertools.islice(fib(), 20)`. **9. Ленивое чтение**: `for line in open(path):` — строка за строкой, без загрузки целиком. **10. Конвейер**: `sum(x*x for x in nums if x%2==0)` (с `islice` для первых 100). **11. Генератор простых**: бесконечный `yield`, проверяя делимость на уже найденные.
</details>

<details><summary>Блок C — ООП (12–16)</summary>

**12. BankAccount**: методы с проверками, `self.history=[]`. **13. Иерархия фигур**: базовый `Shape` с `area()`, переопределяют потомки. **14. Vector**: `__add__`, `__sub__`, `__mul__`, `__eq__`, `__repr__`. **15. __slots__-бенчмарк**: `__slots__=('x','y')` экономит память (нет `__dict__`), замерь `tracemalloc` на 1 млн. **16. Колода карт**: `Card`, `Deck` с `shuffle/deal`, `__len__`, `__getitem__`.
</details>

<details><summary>Блок D — исключения (17–19)</summary>

**17. Безопасный калькулятор**: `try: ... except (ZeroDivisionError, ValueError):`. **18. Валидатор**: свои `class AgeError(Exception)`, `raise`. **19. Retry**: цикл `for _ in range(n): try: return op() except: continue`.
</details>

<details><summary>Блок E — модули и файлы (20–23)</summary>

**20. Многофайловый проект**: пакет с `__init__.py`, `main.py`, venv, `requirements.txt`. **21. JSON-заметки**: `json.load/dump`, CRUD. **22. Анализатор лога**: построчный разбор, `Counter` по уровням. **23. CSV-аналитика**: `csv.DictReader`, агрегаты по колонкам.
</details>

---

## 🧩 Раздел «Проекты и API»

<details><summary>Блоки A–C (1–17)</summary>

**A. Структура (1–5)**: `src/myapp/` с модулями; `__init__.py` реэкспортирует API (`__all__`, `__version__`); приватное — с `_`; `pyproject.toml` + `pip install -e .`; цикл импорта — вынеси общее в отдельный модуль. **B. API (6–10)**: класс с public-методами и `_helpers`; типы + docstring (проверь `mypy`); свои исключения вместо `None`/`print`; `@dataclass` для результата; ревью — понятен ли модуль по именам/типам. **C. Веб-API (11–17)**: `requests.get(url).json()`; параметры через `params=`; обработка `response.raise_for_status()`/`Timeout`/`ConnectionError`; open-meteo по координатам; ключ из `os.environ`; пагинация циклом по страницам; класс-клиент с `requests.Session`, типами, своими исключениями.
```python
class GitHubClient:
    def __init__(self): self._s = requests.Session()
    def user(self, name: str) -> dict:
        r = self._s.get(f"https://api.github.com/users/{name}", timeout=10)
        if r.status_code == 404: raise UserNotFound(name)
        r.raise_for_status(); return r.json()
```
</details>

---

## 🦅 Уровень 4 — Senior

<details><summary>Блок A — память глубоко (1–5)</summary>

**1. Размеры объектов**: таблица `sys.getsizeof` для int/str/list/dict/set/tuple. **2. __slots__-бенчмарк**: `tracemalloc` на 1 млн объектов со слотами и без — экономия в разы. **3. Поиск утечки**: `tracemalloc.start()`, снимки `take_snapshot().compare_to()`. **4. weakref-кэш**: `weakref.WeakValueDictionary()` — значения исчезают при отсутствии других ссылок. **5. Рекурсивный sizeof**: суммируй `getsizeof` всех вложенных элементов.
</details>

<details><summary>Блок B — декораторы и замыкания (6–10)</summary>

**6. Замыкание-счётчик**: `def make(): c=0; def inc(): nonlocal c; c+=1; return c; return inc`. **7. @timed/@logged**: обёртка с `functools.wraps`, замер `time.perf_counter()`. **8. @repeat(n)**: декоратор с аргументом = три уровня вложенности (фабрика → декоратор → обёртка). **9. lru_cache**: `@functools.lru_cache` на рекурсию — резкое ускорение. **10. @validate**: проверка `args` перед вызовом, `raise` при ошибке.
</details>

<details><summary>Блок C — профилирование (11–14)</summary>

**11. timeit-дуэль**: `"".join(list)` сильно быстрее `s += x` в цикле. **12. cProfile**: `cProfile.run('f()')` → ищи большой `cumtime`. **13. memory_profiler**: `@profile` → прожорливая строка. **14. Оптимизация**: профилируй → улучшай → докажи `timeit`.
</details>

<details><summary>Блок D — конкурентность (15–19)</summary>

**15. Докажи GIL**: CPU-задача — 4 потока **не** быстрее 1 (GIL), 4 процесса — быстрее. **16. threading для I/O**: потоки ускоряют I/O (ждут не на CPU). **17. Гонка + Lock**: `with lock: counter += 1`. **18. multiprocessing.Pool**: `Pool().map(f, data)` — реальный параллелизм. **19. asyncio.gather**: `await asyncio.gather(*tasks)` — сравни sync/threads/async на «запросах».
</details>

<details><summary>Блоки E, F — производительность и качество (20–25)</summary>

**20. numpy vs список**: `np.array` быстрее и компактнее на 1 млн. **21. Векторизация**: `a*b+c` на массивах numpy без цикла. **22. numba @njit**: декоратор ускоряет числовую функцию. **23. Аннотации + mypy**: типы на функциях, `mypy .` чисто. **24. pytest**: `def test_x(): assert ...`, `pytest.raises(ValueError)`. **25. ruff+black+logging**: формат, линт, `logging` вместо `print`.
</details>

---

> 📚 Решения других треков — кнопка «✅ Решения» в панели слева на нужном треке.
