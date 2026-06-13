# ✅ Решебник Rust — решения всех задач по категориям

> 🎯 Разборы задач из всех `TASKS.md` трека Rust, по уровням. Сначала реши сам — потом сверься.
> Показан **ключевой код** (идея). Проверяй через `cargo check`/`cargo clippy`/`cargo test`.

> 💡 Раскрывай решения по одному (`▶`). Многие задачи L2 — про **чтение ошибок компилятора**:
> borrow checker учит через ошибки, и это нормально.

---

## 🐣 Уровень 1 — Основы

<details><summary>Блок A — переменные и типы (1–5)</summary>

**1. mut и затенение**: `let mut x=5; x=6;` (мутация) vs `let x=5; let x=x+1;` (новая переменная). **2. Преобразование**: `let f = i as f64;`. **3. Кортеж**: `let t=("Аня",20,165); let (n,a,h)=t;`. **4. Переполнение**: `let x: u8 = 255; x+1` → паника в debug. **5. Обмен**: `std::mem::swap(&mut a, &mut b);`.
</details>

<details><summary>Блок B — функции и поток (6–10)</summary>

**6. square/cube/avg**: `fn square(x: i32) -> i32 { x*x }` (без `;` и `return` — выражение). **7. Знак**: `let s = if n>0 {1} else if n<0 {-1} else {0};`. **8. min_max**: `fn mm(v:&[i32])->(i32,i32){...}` → кортеж. **9. loop со значением**: `let r = loop { i+=1; if i*i>1000 { break i; } };`. **10. Точка с запятой**: `{ x+1; }` возвращает `()` вместо числа → ошибка типа (убери `;`).
</details>

<details><summary>Блок C — match и циклы (11–16)</summary>

**11. FizzBuzz через match**: `match (i%3, i%5) { (0,0)=>..., (0,_)=>"Fizz", (_,0)=>"Buzz", _=>... }`. **12. Категория возраста**: `match age { 0..=17=>"ребёнок", 18..=64=>"взрослый", _=>"пожилой" }`. **13. Калькулятор на match**: `match op { '+'=>a+b, ... }`. **14. Таблица умножения**: вложенные `for i in 1..=9`. **15. Сумма цифр**: `while n>0 { s+=n%10; n/=10; }`. **16. Простые до N**: проверь делители до `√n`.
</details>

<details><summary>Блок D — ввод-вывод и строки (17–21)</summary>

**17. Приветствие**: `io::stdin().read_line(&mut s)?; let name = s.trim();`. **18. Калькулятор-эхо**: `let n: i32 = s.trim().parse().unwrap();`. **19. Конвертер температур**: ввод + формула. **20. Реверс строки**: `s.chars().rev().collect::<String>()`. **21. Палиндром**: `s.chars().eq(s.chars().rev())`.
</details>

---

## 🐥 Уровень 2 — Память (ядро Rust)

<details><summary>Блок A — владение (1–5)</summary>

**1. Move**: `let s2=s1;` → `s1` больше нельзя (перемещено), ошибка «value borrowed after move». **2. Copy**: с `i32` `let b=a;` работает — числа реализуют `Copy` (копируются, не перемещаются). **3. clone**: `let s2=s1.clone();` — две независимые `String`. **4. Функция забирает владение**: `fn take(s: String)` забирает; **фикс** — вернуть `-> String` или брать `&String`. **5. Область видимости**: `String` освобождается в конце `{}` (Drop).
</details>

<details><summary>Блок B — заимствование (6–10)</summary>

**6. &-чтение**: `fn len(s: &String) -> usize { s.len() }`. **7. &mut**: `fn add(s: &mut String) { s.push_str("!"); }`. **8. Три способа**: value (забирает), `&` (читает), `&mut` (меняет) — сравни последствия. **9. Сумма &Vec**: `fn sum(v: &[i32]) -> i32 { v.iter().sum() }`. **10. Убери clone**: передавай `&` вместо `.clone()` там, где значение только читается.
</details>

<details><summary>Блок C — borrow checker (11–14)</summary>

**11. Конфликт &/&mut**: одновременно `&` и `&mut` → ошибка «cannot borrow as mutable because also borrowed as immutable». Правило: один `&mut` ИЛИ много `&`. **12. Висячая ссылка**: `fn f() -> &String { let s=...; &s }` → ошибка (s умрёт); **фикс** — верни `String` (владение). **13. NLL**: после последнего использования `&` можно брать `&mut` (заём «заканчивается» на последнем использовании). **14. Изменение в итерации**: нельзя `push` в `Vec` во время `for &x in &v` — итератор держит `&`, а `push` требует `&mut`.
</details>

<details><summary>Блок D — строки и слайсы (15–19)</summary>

**15. String vs &str**: `String` владеет (куча), `&str` — заём (срез). **16. first_word**: `fn first_word(s: &str) -> &str { &s[..s.find(' ').unwrap_or(s.len())] }`. **17. &str-параметр**: `fn f(s: &str)` принимает и `String` (через `&`), и литерал. **18. байты vs символы**: на кириллице `"привет".len()` (байты, UTF-8) ≠ `.chars().count()` (символы). **19. Слайс и borrow**: пока жив слайс `&s[..]`, источник нельзя менять (`&mut`).
</details>

<details><summary>Блок E — времена жизни (20–21)</summary>

**20. longest**: `fn longest<'a>(a: &'a str, b: &'a str) -> &'a str { if a.len()>b.len() {a} else {b} }`. **21. Структура со ссылкой**: `struct Excerpt<'a> { part: &'a str }` — живёт не дольше источника.
</details>

---

## 🐥 Уровень 3 — Middle

<details><summary>Блок A — структуры (1–4)</summary>

**1. Rectangle**: `impl Rectangle { fn new(...)->Self{...} fn area(&self)->f64{...} }`. **2. Point + derive**: `#[derive(Debug,Clone,PartialEq)] struct Point{x:f64,y:f64}`, `distance` через `hypot`. **3. BankAccount**: методы `deposit/withdraw/balance`. **4. newtype**: `struct Celsius(f64);` с методом в `Fahrenheit`.
</details>

<details><summary>Блок B — enum и Option (5–8)</summary>

**5. TrafficLight**: `enum Light{Red,Yellow,Green}`, `next` через `match`. **6. Shape enum**: `match` по вариантам → площадь. **7. Безопасное деление**: `fn div(a,b)->Option<f64>{ if b==0.0 {None} else {Some(a/b)} }`. **8. Поиск**: `-> Option<usize>` (`None` если не найдено).
</details>

<details><summary>Блок C — обработка ошибок (9–11)</summary>

**9. divide → Result**: `fn div(a,b)->Result<f64,String>{ if b==0.0 {Err("деление на 0".into())} else {Ok(a/b)} }`. **10. parse через ?**: `let n: i32 = s.parse()?;`. **11. Цепочка ?**: чтение+парсинг+вычисление, каждый `?` пробрасывает ошибку вверх.
</details>

<details><summary>Блок D — обобщения и трейты (12–15)</summary>

**12. largest<T>**: `fn largest<T: PartialOrd + Copy>(v: &[T]) -> T {...}`. **13. Трейт Shape**: `trait Shape{ fn area(&self)->f64; }` для Circle/Rectangle. **14. Display**: `impl fmt::Display for Point { fn fmt(...){ write!(f,"({},{})",self.x,self.y) } }`. **15. Stack<T>**: `struct Stack<T>{ d: Vec<T> }` с `push/pop/peek`.
</details>

<details><summary>Блок E — коллекции (16–20)</summary>

**16. Vec**: `v.iter().sum()`, `.max()`, `.iter_mut().for_each(|x|*x*=2)`. **17. Частота слов**: `*map.entry(word).or_insert(0) += 1`. **18. Уникальные**: `HashSet`. **19. Телефонная книга**: `HashMap<String,String>`. **20. Топ-N**: собрать в `Vec`, отсортировать по значению, взять N.
</details>

<details><summary>Блок F — замыкания и итераторы (21–24)</summary>

**21. map/filter/collect**: `v.iter().filter(|&&x|x>0).map(|x|x*2).collect::<Vec<_>>()`. **22. Конвейер текста**: цепочка `split → filter → map → collect`. **23. fold**: `v.iter().fold(1, |acc,x| acc*x)`. **24. Среднее/медиана**: `sum/len`; медиана — отсортировать и взять середину.
</details>

---

## 🧩 Раздел «Проекты и API»

<details><summary>Блоки A–C (1–15)</summary>

**A. Структура (1–5)**: `mod math;` (файл `math.rs`); `pub` открывает, приватное по умолчанию (доступ к приватному → ошибка); логика в `lib.rs`, использование из `main.rs`; папка-модуль `shapes/mod.rs` с подмодулями; workspace — `[workspace]` в корневом `Cargo.toml` с членами-крейтами. **B. API (6–10)**: приватные поля + `pub fn` доступа; `trait Storage` с двумя реализациями; свой `enum Error` + `impl Display`/`Error`, возврат `Result`; **Builder** — методы возвращают `self`, финальный `build()`; doc-тесты — `///` с примером, `cargo test` их прогонит. **C. Веб-API (11–15)**: `reqwest::blocking::get(url)?`; `#[derive(Deserialize)] struct Weather{...}` + `.json()?`; обработка 404/сети через `?` и `Result`; open-meteo в структуру; `struct Client` с типизированными методами.
```rust
#[derive(Deserialize)]
struct User { login: String, public_repos: u32 }
fn user(name: &str) -> Result<User, reqwest::Error> {
    reqwest::blocking::get(format!("https://api.github.com/users/{name}"))?.json()
}
```
</details>

---

## 🦅 Уровень 4 — Senior

<details><summary>Блок A — умные указатели (1–5)</summary>

**1. Box + рекурсивный список**: `enum List{ Cons(i32, Box<List>), Nil }` (Box даёт известный размер). **2. Rc + strong_count**: `Rc::clone(&a)` увеличивает `Rc::strong_count`. **3. RefCell**: `borrow_mut()` дважды одновременно → паника в рантайме (проверка заимствования перенесена в рантайм). **4. Rc<RefCell>**: разделяемая изменяемость для дерева/графа. **5. Weak**: ребёнок держит `Weak` на родителя → нет цикла → нет утечки.
</details>

<details><summary>Блок B — многопоточность (6–11)</summary>

**6. Поток + join**: `let h = thread::spawn(|| {...}); h.join().unwrap();`. **7. move в поток**: `thread::spawn(move || { use(data); })`. **8. Попытка гонки → ошибка компиляции**: использовать общие данные без `Arc/Mutex` → компилятор не пропустит (Rust ловит гонки на этапе сборки!). **9. Arc<Mutex>**: `let c = Arc::new(Mutex::new(0));` → в каждом потоке `*c.lock().unwrap() += 1`. **10. Параллельная сумма**: раздели срез по потокам, сложи частичные. **11. Каналы**: `let (tx, rx) = mpsc::channel();` — producer шлёт, consumer принимает.
</details>

<details><summary>Блок C — трейты (12–15)</summary>

**12. Box<dyn Trait>**: `Vec<Box<dyn Shape>>` — разные типы в одном векторе. **13. Свой Iterator**: `impl Iterator for X { type Item=...; fn next(&mut self)->Option<...> {...} }`. **14. Add для Vector2D**: `impl Add for Vec2 { type Output=Vec2; fn add(self,o:Vec2)->Vec2{...} }`. **15. Система команд**: `Vec<Box<dyn Command>>`, у каждой `execute()`.
</details>

<details><summary>Блоки D, E, F — unsafe, производительность, качество (16–23)</summary>

**16. Сырые указатели**: `unsafe { let p = &x as *const i32; *p }`. **17. FFI**: `extern "C" { fn abs(i: i32) -> i32; }`, вызов в `unsafe`. **18. debug vs release**: `cargo run --release` многократно быстрее. **19. Итератор vs цикл**: одинаковая скорость (zero-cost abstractions). **20. flamegraph**: профиль `cargo flamegraph` — узкое место. **21. Тесты**: `#[test] fn t(){ assert_eq!(...); }`, `#[should_panic]`. **22. clippy+fmt+doc**: `cargo clippy && cargo fmt && cargo doc`. **23. async с tokio**: `#[tokio::main] async fn main()`, `.await`.
</details>

---

> 📚 Решения других треков — кнопка «✅ Решения» в панели слева на нужном треке.
