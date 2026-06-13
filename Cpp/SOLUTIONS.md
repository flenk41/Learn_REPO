# ✅ Решебник C++ — решения всех задач по категориям

> 🎯 Разборы задач из всех `TASKS.md` трека C++, по уровням. Сначала реши сам — потом сверься.
> Показан **ключевой код** (идея). Компилируй с `g++ -std=c++17 -Wall -Wextra -fsanitize=address`.

> 💡 Раскрывай решения по одному (`▶`).

---

## 🐣 Уровень 1 — Основы C++

<details><summary>Блок A — типы и ввод-вывод (1–5)</summary>

**1. Визитка**: `std::cout << "Имя\tКирилл\n" << "Город\tМосква\n";`
**2. Обмен**: `std::swap(a,b);` или вручную через `int t=a; a=b; b=t;`.
**3. Конвертер км→мили**: `std::cout << std::fixed << std::setprecision(2) << km*0.621;`
**4. auto**: `auto i=5; auto d=5.0; auto s="hi";` — типы `int`, `double`, `const char*`; проверь `typeid(i).name()` или наведением IDE.
**5. Сужающая инициализация**: `int x{3.9};` — фигурные скобки **запрещают** сужение → ошибка компиляции (в отличие от `int x=3.9;`, где молча 3).
</details>

<details><summary>Блок B — условия (6–9)</summary>

**6. Тип треугольника**: сначала существование (`a+b>c && ...`), потом `==` сторон (см. решебник C, №5).
**7. Квадратное уравнение**: дискриминант + случаи `a==0`, `D>0/==0/<0` (см. решебник C, №7).
**8. Калькулятор на switch**: `switch(op){ case '+': ...; case '/': if(b==0) ...; }`.
**9. КНБ**: выигрышные пары через условие (см. решебник C, №8).
</details>

<details><summary>Блок C — циклы (10–15)</summary>

**10. Сумма цифр**: `while(n){ s+=n%10; n/=10; }`
**11. FizzBuzz**: `for(i=1;i<=100;i++) cout << (i%15?i%3?i%5?to_string(i):"Buzz":"Fizz":"FizzBuzz") << "\n";` (или явные if).
**12. Фибоначчи**: `long a=0,b=1; for(...){ cout<<a<<' '; auto t=a+b; a=b; b=t; }`
**13. range-for сумма/макс vector**: `for(int x: v){ sum+=x; mx=max(mx,x); }`
**14. Удвоение на месте**: `for(auto& x: v) x*=2;` — `auto&` (ссылка!) меняет элементы.
**15. Решето Эратосфена**: `vector<bool> p(N+1,true); for(int i=2;i*i<=N;i++) if(p[i]) for(int j=i*i;j<=N;j+=i) p[j]=false;`
</details>

<details><summary>Блок D — функции (16–20)</summary>

**16. swap по ссылке + перегрузка**: `void sw(int&a,int&b){...}` и `void sw(double&a,double&b){...}` — компилятор выберет по типу.
**17. minmax через tuple**: `std::tuple<int,int> mm(...){ return {mn,mx}; }` → `auto [lo,hi] = mm(v);`
**18. max3/is_prime/factorial**: `bool is_prime(int n){ if(n<2)return false; for(int i=2;i*i<=n;i++) if(n%i==0)return false; return true; }`
**19. print по const&**: `void print(const std::string& s){ cout<<s; }` — без копии.
**20. Калькулятор с перегрузкой**: `int add(int,int)` и `double add(double,double)` — выбор по типам аргументов.
</details>

---

## 🐥 Уровень 2 — Память (ASan!)

<details><summary>Блок A — ссылки (1–4)</summary>

**1. Псевдоним**: `int x=5; int& r=x; r=10;` → x стал 10. **2. swap по ссылке**: `void sw(int&a,int&b){int t=a;a=b;b=t;}`. **3. Сумма по const&**: `int sum(const vector<int>& v){...}` — без копии. **4. Ссылка vs указатель**: `r=10;` (ссылка) vs `*p=10;` (указатель) — ссылка короче и не бывает null.
</details>

<details><summary>Блок B — new/delete и опасности (5–8)</summary>

**5. new/delete**: `int* p=new int(5); delete p; int* a=new int[10]; delete[] a;` (массив — `delete[]`!). **6. Утечка**: `new` без `delete` → ASan покажет leak. **7. use-after-free/double-free**: обращение/`delete` после `delete` → ASan ловит. **8. Исключение ломает delete**: если между `new` и `delete` бросок — утечка; **фикс**: `vector`/`unique_ptr` (RAII освободит при размотке стека).
</details>

<details><summary>Блок C — RAII (9–13)</summary>

**9. Класс с деструктором**: `~Foo(){ cout<<"destroyed"; }` — вызовется автоматически в конце области. **10. Порядок LIFO**: объекты разрушаются в обратном порядке создания. **11. RAII-массив**: класс с `new[]` в конструкторе и `delete[]` в деструкторе — ASan чист. **12. RAII при исключении**: деструктор вызывается при размотке стека. **13. RAII-файл**:
```cpp
struct File{ FILE* f; File(const char*p){ f=fopen(p,"r"); } ~File(){ if(f)fclose(f); } };
```
</details>

<details><summary>Блок D — умные указатели (14–18)</summary>

**14. unique_ptr**: `auto p = std::make_unique<int>(5);` — освободится сам. **15. move владения**: `auto q = std::move(p);` — теперь `p==nullptr`. **16. shared_ptr + use_count**: `auto a=make_shared<int>(1); auto b=a; cout<<a.use_count();` → 2. **17. Цикл shared_ptr**: два объекта ссылаются `shared_ptr` друг на друга → утечка; **фикс**: один из них держит `weak_ptr`. **18. Список на unique_ptr**: `struct Node{ int v; unique_ptr<Node> next; };` — освобождение каскадом, без ручного delete.
</details>

<details><summary>Блок E — move (19–20)</summary>

**19. Move vs копия**: на большом `vector` `auto b = std::move(a);` мгновенно (переставляет указатели), копия — линейно. **20. push_back с move**: `v.push_back(std::move(s));` — `s` становится пустой (содержимое «украдено»).
</details>

---

## 🐥 Уровень 3 — Middle

<details><summary>Блок A — классы (1–5)</summary>

**1. Point/Rect/Circle**: приватные поля + public-методы `area()`. **2. BankAccount**: `deposit/withdraw` с проверкой баланса, `vector<string> history`. **3. Правило пяти**: класс с `new[]` без копирующего конструктора → двойное освобождение (краш); **фикс**: определить копирующий/перемещающий конструктор+оператор+деструктор. **4. Правило нуля**: заменить `new[]` на `vector` → копирование/перемещение/очистка «бесплатны». **5. Time**: нормализация через секунды (см. решебник C, №4 L3).
</details>

<details><summary>Блок B — наследование (6–8)</summary>

**6. Иерархия животных**: `struct Animal{ virtual string speak()=0; };` → `Dog::speak(){return "Гав";}`. **7. Виртуальный деструктор**: удаление через `Base*` без `virtual ~Base()` → деструктор потомка не вызван → утечка (ASan); **фикс**: `virtual ~Base()`. **8. Фигуры**: `vector<unique_ptr<Shape>>`, цикл `for(auto& s: shapes) total += s->area();`.
</details>

<details><summary>Блок C — шаблоны (9–11)</summary>

**9. maxValue/swap**: `template<class T> T maxv(T a,T b){ return a>b?a:b; }`. **10. Box<T>**: `template<class T> struct Box{ T value; };`. **11. Stack<T>**:
```cpp
template<class T> struct Stack{ vector<T> d;
  void push(T x){ d.push_back(x); } T pop(){ T t=d.back(); d.pop_back(); return t; }
  T& top(){ return d.back(); } bool empty(){ return d.empty(); } };
```
</details>

<details><summary>Блок D — STL (12–16)</summary>

**12. vector**: `accumulate`, `*min_element`, `*max_element`, `for(auto&x:v)x*=2`. **13. Частота слов**: `unordered_map<string,int> f; f[word]++;`. **14. Уникальные**: `set<string> s(words.begin(),words.end());`. **15. Телефонная книга**: `map<string,string>`. **16. Анаграммы**: ключ = отсортированное слово, `map<string, vector<string>>`.
</details>

<details><summary>Блок E — алгоритмы и лямбды (17–19)</summary>

**17. sort/accumulate/transform**: `sort(v.begin(),v.end()); transform(v.begin(),v.end(),v.begin(),[](int x){return x*x;});`. **18. count_if/copy_if**: `count_if(v.begin(),v.end(),[](int x){return x%2==0;});`. **19. Сортировка структур**: `sort(v.begin(),v.end(),[](auto&a,auto&b){return a.price<b.price;});`.
</details>

<details><summary>Блок F — операторы (20–22)</summary>

**20. Vector2D**: `Vec operator+(const Vec&o)const{ return {x+o.x,y+o.y}; }`, также `-`, `*` (скаляр), `==`. **21. Fraction**: арифметика с приведением к общему знаменателю + сокращение (НОД), `operator<<`. **22. Matrix**: `+`, `*` (классическое умножение), `operator<<` для печати.
</details>

---

## 🧩 Раздел «Проекты и API»

<details><summary>Блоки A–C (1–15)</summary>

**A. Структура (1–5)**: вынеси класс в `.hpp/.cpp`; CMake с `include/ src/`; `add_library` для логики; анонимный `namespace {}` прячет от внешних файлов; три модуля без циклов зависимостей. **B. API (6–10)**: public-методы + private-поля; владение через `unique_ptr`(владеет)/`const&`(одолжен)/`optional`(может не быть); `const` на неизменяющих методах; **pImpl** — `class Foo{ struct Impl; unique_ptr<Impl> p; };` (реализация скрыта в `.cpp`); API-ревью — понятен ли `.hpp` без `.cpp`. **C. Веб-API (11–15)**: `cpr::Get(cpr::Url{...})` → `.status_code`, `.text`; `nlohmann::json::parse(text)["field"]`; проверь 404/сеть/`try{json::parse}catch`; open-meteo по координатам; класс-обёртка `WeatherClient` с методом `current(lat,lon) -> Weather`.
</details>

---

## 🦅 Уровень 4 — Senior

<details><summary>Блок A — move глубоко (1–4)</summary>

**1. Перемещающий конструктор**: `Foo(Foo&& o) noexcept : data(o.data){ o.data=nullptr; }`. **2. noexcept-move**: без `noexcept` `vector` при росте **копирует** (ради гарантии исключений); с `noexcept` — перемещает. **3. Правило нуля**: на `vector`/`unique_ptr` все спецфункции не нужны. **4. RVO**: возврат локального объекта не копируется (компилятор строит на месте) — докажи отсутствием вывода копирующего конструктора.
</details>

<details><summary>Блок B — память (5–7)</summary>

**5. Padding**: переставь поля по убыванию размера, докажи `sizeof`. **6. Свой operator new**: `void* operator new(size_t n){ cout<<"alloc "<<n; return malloc(n); }`. **7. Pool-аллокатор**: блоки фикс. размера + free-list, замер против `new` (быстрее — нет системных вызовов).
</details>

<details><summary>Блок C — многопоточность (8–10)</summary>

**8. Гонка**: `count++` из потоков без защиты → TSan; **фикс** `std::mutex`+`lock_guard` или `std::atomic<int>`. **9. Параллельная сумма через async**: `auto f = std::async([&]{...}); sum += f.get();`. **10. Пул потоков**: очередь задач + `mutex` + `condition_variable`, рабочие берут задачи.
</details>

<details><summary>Блок D — шаблоны/мета (11–13)</summary>

**11. constexpr факториал**: `constexpr int fact(int n){ return n<2?1:n*fact(n-1); } int a[fact(5)];`. **12. Вариативный sum**: `template<class...A> auto sum(A...a){ return (a+...); }` (fold expression). **13. Концепт (C++20)**: `template<class T> requires std::integral<T> T f(T x){...}`.
</details>

<details><summary>Блоки E, F — производительность и современный (14–19)</summary>

**14. vector vs list**: обход `vector` быстрее (локальность кэша), замер `chrono`. **15. Копия vs const&**: передача большого объекта по `const&` без копии. **16. Оптимизация**: профилируй, улучшай, докажи `chrono`. **17. optional**: `std::optional<int> find(...)` вместо «-1». **18. ranges (C++20)**: `v | std::views::filter(...) | std::views::transform(...)`. **19. CMake+санитайзеры+clang-tidy**: добавь флаги и линтер в сборку.
</details>

---

> 📚 Решения других треков — кнопка «✅ Решения» в панели слева на нужном треке.
