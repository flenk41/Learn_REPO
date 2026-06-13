# ✅ Решебник C — решения всех задач по категориям

> 🎯 Здесь собраны **разборы и решения** задач из всех `TASKS.md` трека C, сгруппированные по
> уровням. Сначала реши сам — потом сверься. Показан **ключевой код** (идея), без обвязки
> `#include`/`main`, если она очевидна. Компилируй с `gcc -Wall -Wextra -fsanitize=address -g`.

> 💡 Раскрывай решения по одному (`▶`), чтобы случайно не подсмотреть лишнее.

---

## 🐣 Уровень 1 — Основы

### Блок A — переменные и ввод-вывод
<details><summary>1–4 · показать решения</summary>

**1. Визитка** — экранирование `\n`/`\t`:
```c
printf("Имя:\tКирилл\nГород:\tМосква\nЯзык:\tC\n");
```
**2. Обмен значений** — через временную переменную:
```c
int t = a; a = b; b = t;   // (без temp: a^=b; b^=a; a^=b; — но temp понятнее)
```
**3. Возраст в днях** — умножение:
```c
long days = (long)years*365, hours = days*24, mins = hours*60;
```
**4. Размен монет** — жадный через `/` и `%`:
```c
int n50=s/50; s%=50; int n10=s/10; s%=10; int n5=s/5; s%=5; int n1=s; // s — копейки
```
</details>

### Блок B — условия
<details><summary>5–8 · показать решения</summary>

**5. Тип треугольника** — сначала существование (неравенство треугольника), потом равенства сторон:
```c
if (a+b<=c || a+c<=b || b+c<=a) puts("не существует");
else if (a==b && b==c) puts("равносторонний");
else if (a==b || b==c || a==c) puts("равнобедренный");
else puts("разносторонний");
```
**6. Время суток** — диапазоны часа:
```c
if (h<6) puts("ночь"); else if (h<12) puts("утро");
else if (h<18) puts("день"); else puts("вечер");
```
**7. Корни квадратного** — дискриминант + крайние случаи:
```c
if (a==0){ if(b) printf("x=%g\n",-c/b); else puts(c? "нет":"любое"); }
else { double D=b*b-4*a*c;
  if (D>0) printf("%g %g\n",(-b+sqrt(D))/(2*a),(-b-sqrt(D))/(2*a));
  else if (D==0) printf("%g\n",-b/(2*a)); else puts("нет действительных"); }
```
**8. Камень-ножницы-бумага** — выигрышные пары:
```c
if (p1==p2) puts("ничья");
else if ((p1==1&&p2==2)||(p1==2&&p2==3)||(p1==3&&p2==1)) puts("игрок 1"); // 1кам 2нож 3бум
else puts("игрок 2");
```
</details>

### Блок C — циклы
<details><summary>9–14 · показать решения</summary>

**9. Сумма цифр** — `%10` и `/10`:
```c
int s=0; while(n){ s+=n%10; n/=10; }
```
**10. Палиндром-число** — развернуть и сравнить (или сравнивать с краёв). Реверс:
```c
int r=0,t=n; while(t){ r=r*10+t%10; t/=10; } puts(r==n? "да":"нет");
```
**11. Таблица степеней двойки** — сдвиг или умножение:
```c
for(int i=0;i<=10;i++) printf("2^%d = %d\n", i, 1<<i);
```
**12. НОД (Евклид)**:
```c
while(b){ int t=a%b; a=b; b=t; } // a — НОД
```
**13. Фибоначчи (цикл)**:
```c
long a=0,b=1; for(int i=0;i<N;i++){ printf("%ld ",a); long t=a+b; a=b; b=t; }
```
**14. Шахматная доска 8×8** — чётность суммы индексов:
```c
for(int i=0;i<8;i++){ for(int j=0;j<8;j++) putchar((i+j)%2? ' ':'#'); putchar('\n'); }
```
</details>

### Блок D — функции
<details><summary>15–18 · показать решения</summary>

**15. max3/min3/average3**:
```c
int max3(int a,int b,int c){ int m=a>b?a:b; return m>c?m:c; }
double average3(int a,int b,int c){ return (a+b+c)/3.0; }
```
**16. Калькулятор на функциях** — по одной функции на операцию; деление с проверкой нуля:
```c
double add(double a,double b){return a+b;}  double divf(double a,double b){return b? a/b:0;}
```
**17. Совершенное число** — сумма делителей:
```c
int is_perfect(int n){ int s=0; for(int d=1;d<n;d++) if(n%d==0) s+=d; return s==n; }
// 6, 28, 496, 8128
```
**18. Ханойские башни (рекурсия)**:
```c
void hanoi(int n,char from,char to,char via){
  if(!n) return; hanoi(n-1,from,via,to);
  printf("%c->%c\n",from,to); hanoi(n-1,via,to,from); }
```
</details>

---

## 🐥 Уровень 2 — Память (компилируй с ASan!)

### Блок A — указатели
<details><summary>1–5 · показать решения</summary>

**1. Три значения через указатели**:
```c
void calc(int a,int b,int*sum,int*dif,int*pro){ *sum=a+b; *dif=a-b; *pro=a*b; }
```
**2. swap для разных типов** — тело одинаково, меняется только тип:
```c
void swap_int(int*a,int*b){ int t=*a; *a=*b; *b=t; }   // аналогично double, char
```
**3. Сортировка пузырьком + swap**:
```c
for(int i=0;i<n-1;i++) for(int j=0;j<n-1-i;j++) if(a[j]>a[j+1]) swap_int(&a[j],&a[j+1]);
```
**4. min/max за один проход**:
```c
void minmax(int*a,int n,int*mn,int*mx){ *mn=*mx=a[0];
  for(int i=1;i<n;i++){ if(a[i]<*mn)*mn=a[i]; if(a[i]>*mx)*mx=a[i]; } }
```
**5. Указатель на середину** — арифметика указателей:
```c
int* middle(int*a,int n){ return a + n/2; }
```
</details>

### Блок B — строки (свои реализации, без `<string.h>`)
<details><summary>6–13 · показать решения</summary>

```c
size_t my_strlen(const char*s){ const char*p=s; while(*p)p++; return p-s; }              // 6
char* my_strcpy(char*d,const char*s){ char*r=d; while((*d++=*s++)); return r; }          // 7
int my_strcmp(const char*a,const char*b){ while(*a&&*a==*b){a++;b++;} return *a-*b; }     // 8
char* my_strcat(char*d,const char*s){ char*r=d; while(*d)d++; while((*d++=*s++)); return r; } // 9
void my_strrev(char*s){ size_t i=0,j=my_strlen(s); if(j)j--;                              // 10
  while(i<j){ char t=s[i]; s[i++]=s[j]; s[j--]=t; } }
int count_ch(const char*s,char c){ int n=0; while(*s) if(*s++==c)n++; return n; }          // 11
char* my_strstr(const char*h,const char*n){                                               // 12
  for(;*h;h++){ const char*a=h,*b=n; while(*b&&*a==*b){a++;b++;} if(!*b) return (char*)h; }
  return *n? NULL:(char*)h; }
// 13 Удаление лишних пробелов на месте: два указателя — чтения и записи, схлопывая повторы.
void squeeze_spaces(char*s){ char*w=s; int sp=0;
  for(char*r=s;*r;r++){ if(*r==' '){ if(!sp)*w++=' '; sp=1; } else { *w++=*r; sp=0; } }
  *w=0; }
```
</details>

### Блок C — динамическая память
<details><summary>14–19 · показать решения (всё через malloc/realloc + free)</summary>

**14. Дубликат массива**:
```c
int* dup(const int*a,int n){ int*b=malloc(n*sizeof*b); for(int i=0;i<n;i++)b[i]=a[i]; return b; }
```
**15. Слияние массивов** — `malloc((n+m))`, скопировать оба подряд.
**16. Фильтр чётных** — два прохода (посчитать → выделить) или `realloc` по ходу:
```c
int* evens(const int*a,int n,int*out){ int*r=NULL,k=0;
  for(int i=0;i<n;i++) if(a[i]%2==0){ r=realloc(r,(k+1)*sizeof*r); r[k++]=a[i]; }
  *out=k; return r; }
```
**17. Своя getline** — расширяй буфер `realloc` при заполнении:
```c
char* my_getline(void){ size_t cap=8,len=0; char*buf=malloc(cap); int c;
  while((c=getchar())!=EOF && c!='\n'){ if(len+1>=cap){ cap*=2; buf=realloc(buf,cap);} buf[len++]=c; }
  buf[len]=0; return buf; }
```
**18. split** — массив динамических строк; не забудь освободить каждый и сам массив.
**19. Транспонирование матрицы** — `b[j][i]=a[i][j]`; освобождай обе (каждую строку + массив строк).
> ⚠️ Каждый `malloc` ↔ ровно один `free`. ASan должен молчать.
</details>

### Блок D — структуры данных на указателях
<details><summary>20–22 · показать решения</summary>

**20. Стек на массиве**:
```c
typedef struct{ int*d; int top,cap; } Stack;
void push(Stack*s,int x){ if(s->top==s->cap){ s->cap*=2; s->d=realloc(s->d,s->cap*sizeof(int)); } s->d[s->top++]=x; }
int pop(Stack*s){ return s->d[--s->top]; }   int peek(Stack*s){ return s->d[s->top-1]; }
```
**21. Динамический вектор** — это пет-проект уровня (см. PROJECT.md): push с ростом ёмкости ×2, get, free.
**22. Односвязный список**:
```c
typedef struct Node{ int v; struct Node*next; } Node;
Node* push_front(Node*h,int v){ Node*n=malloc(sizeof*n); n->v=v; n->next=h; return n; }
void free_list(Node*h){ while(h){ Node*t=h->next; free(h); h=t; } }
```
</details>

---

## 🐥 Уровень 3 — Middle

### Блок A — структуры
<details><summary>1–4 · показать решения</summary>

**1. Геометрия**: `typedef struct{double x,y;}Point;` площадь круга `M_PI*r*r`, попадание точки в круг — расстояние ≤ r. **2. Complex**: сложение покомпонентно, модуль `hypot(re,im)`. **3. Каталог**: массив `Product`, сортировка `qsort` по цене, сумма склада циклом. **4. Time**: всё в секунды → арифметика → обратно (`s%60`, `m%60`).
```c
typedef struct{int h,m,s;}Time;
Time norm(int total){ return (Time){ total/3600, total/60%60, total%60 }; }
```
</details>

### Блок B — структуры данных
<details><summary>5–9 · показать решения</summary>

**5. Связный список** — полный набор (см. L2 №22 + разворот: переставляй `next` назад). **6. Проверка скобок стеком**: открывающую — push, закрывающую — сверить с pop; в конце стек пуст. **7. Очередь**: голова/хвост, enqueue в хвост, dequeue из головы. **8. Дерево поиска (BST)**:
```c
Node* insert(Node*t,int v){ if(!t){ t=malloc(sizeof*t); t->v=v; t->l=t->r=NULL; }
  else if(v<t->v) t->l=insert(t->l,v); else t->r=insert(t->r,v); return t; }
void inorder(Node*t){ if(t){ inorder(t->l); printf("%d ",t->v); inorder(t->r);} }
```
**9. Хеш-таблица (chaining)**: массив списков, индекс = `hash(key)%size`; put/get/remove идут по списку в бакете.
</details>

### Блок C — указатели на функции
<details><summary>10–12 · показать решения</summary>

**10. map/filter/reduce**:
```c
void map(int*a,int n,int(*f)(int)){ for(int i=0;i<n;i++) a[i]=f(a[i]); }
int reduce(int*a,int n,int(*f)(int,int),int acc){ for(int i=0;i<n;i++) acc=f(acc,a[i]); return acc; }
```
**11. qsort по полям**: компаратор на каждое поле, `qsort(arr,n,sizeof,cmp_by_price)`. **12. Мини-CLI**: `struct{char*name; void(*fn)(void);} cmds[]`, цикл — найти имя, вызвать `fn`.
</details>

### Блок D — файлы и модульность
<details><summary>13–16 · показать решения</summary>

**13. wc**: читай по символам, считай символы; `\n` → строки; переход непробел→пробел → слова. **14. CSV→структуры**: `fgets` строку, `strtok` по запятой → поля. **15. Лог**: `fopen(path,"a")`, пиши с `time()`/`ctime`. **16. Многофайловый проект**: вынеси логику в `foo.h`/`foo.c`, Makefile с правилами `.o` и линковкой.
</details>

### Блок E — биты
<details><summary>17–20 · показать решения</summary>

**17. Двоичное + подсчёт единиц**:
```c
for(int i=31;i>=0;i--) putchar((n>>i&1)+'0');
int ones=0; for(unsigned t=n;t;t&=t-1) ones++;   // трюк Кернигана
```
**18. Права-флаги**: выдать `f|=READ`, отнять `f&=~READ`, проверить `f&READ`. **19. XOR-шифр**: `c ^= key[i%len]` (повторное применение расшифрует). **20. Упаковка RGB**: `(r<<16)|(g<<8)|b`; распаковка `(x>>16)&0xFF` и т.д.
</details>

---

## 🧩 Раздел «Проекты и API»

<details><summary>Блок A–C · показать решения</summary>

**A. Структура проекта (1–4)**: вынеси логику из `main.c` в модуль `.h/.c`; разложи `include/ src/ build/`, в Makefile `-Iinclude`; `static` делает функцию приватной для файла (извне недоступна — будет ошибка линковки); три модуля — следи, чтобы зависимости шли в одну сторону (нет циклов `#include`).
**B. Проектирование API (5–9)**: opaque-тип — в `.h` только `typedef struct Stack Stack;` (без полей), определение `struct` — в `.c`; парный `create`/`destroy`; единый стиль ошибок (например, возвращать `int`-код или enum); `const` на всех входных указателях, которые не меняются; API-ревью — дай заголовок коллеге, собери замечания.
**C. Внешние API (10–13)**: libcurl `curl_easy_*` для GET, проверь `CURLcode` и HTTP-код (`CURLINFO_RESPONSE_CODE`); 200 — успех, 404 — нет ресурса; cJSON `cJSON_Parse` → `cJSON_GetObjectItem` для полей; оберни всё в чистую функцию `fetch(url, &result)`.
</details>

---

## 🦅 Уровень 4 — Senior

<details><summary>Блок A — аллокаторы (1–4)</summary>

**1. Arena**: один большой буфer + указатель-смещение; alloc двигает смещение (с выравниванием), free всей арены разом. **2. Pool**: блоки фиксированного размера + free-list (список свободных). **3. Список на пуле**: узлы из пула — быстрее malloc (нет системных вызовов на каждый узел). **4. Свой malloc**: free-list блоков с заголовками (размер+флаг), при free — слияние соседних свободных (coalescing).
```c
void* arena_alloc(Arena*a,size_t n){ size_t p=(a->off+15)&~(size_t)15; // align 16
  if(p+n>a->cap) return NULL; a->off=p+n; return a->buf+p; }
```
</details>

<details><summary>Блок B — память и UB (5–7)</summary>

**5. Padding**: переставь поля от больших к меньшим — меньше дыр выравнивания; докажи `sizeof`. **6. align_up**: `(x + a-1) & ~(a-1)` для степени двойки a. **7. UBSan-охота**: переполнение int, сдвиг на ширину типа, разыменование NULL, выход за массив, знаковое переполнение — каждый ловится `-fsanitize=undefined`.
</details>

<details><summary>Блок C — многопоточность (8–11)</summary>

**8. Гонка**: два потока `count++` без защиты → итог < ожидаемого, TSan укажет. **9. Починка**: `pthread_mutex_lock/unlock` вокруг инкремента, или `atomic_fetch_add`; атомик обычно быстрее для счётчика. **10. Параллельная сумма**: раздели массив на N частей, каждый поток суммирует свою, потом сложи частичные. **11. Пул потоков**: очередь задач + мьютекс + условная переменная; рабочие потоки берут задачи из очереди.
</details>

<details><summary>Блок D — кэш и оптимизация (12–14)</summary>

**12. Матрица строки vs столбцы**: обход по строкам быстрее (локальность кэша, данные идут подряд); замерь `clock()`. **13. AoS vs SoA**: при обработке одного поля SoA быстрее (плотно в кэше). **14. Оптимизация**: профилируй (`perf`), найди горячую точку, улучшай её, докажи замером «до/после».
</details>

<details><summary>Блоки E, F — система и инструменты (15–20)</summary>

**15. mmap**: `mmap(NULL,len,PROT_READ,MAP_PRIVATE,fd,0)` — файл как память. **16. fork/exec**: `fork()`, в потомке `execvp(cmd,args)`, в родителе `wait`. **17. TCP эхо-сервер**: `socket/bind/listen/accept`, читай и отсылай обратно (см. трек Сети, модуль 17). **18. GDB watchpoint**: `watch var` — остановка при изменении, находит, кто портит память. **19. perf/gprof**: показывает, где жжётся CPU. **20. Аудит**: прогон через `-Wall -Wextra -fsanitize=address,undefined` + valgrind + perf.
</details>

---

> 📚 Решения остальных треков — кнопка «✅ Решения» в панели слева на соответствующем треке.
> Не нашёл задачу? Сверься с номером в [TASKS.md](01-basics/TASKS.md) нужного уровня.
