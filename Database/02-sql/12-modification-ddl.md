# 12 · Изменение данных и DDL 🖼️⭐

> 🎯 **Цель блока:** освоить изменение данных (INSERT/UPDATE/DELETE) и управление структурой
> (CREATE/ALTER/DROP) — полный набор SQL-команд.

---

## 📖 DML: изменение данных

```sql
-- INSERT — добавить строки:
INSERT INTO clients (name, email) VALUES ('Анна', 'anna@mail.com');
INSERT INTO clients (name, email) VALUES ('Иван', 'i@mail.com'), ('Олег', 'o@mail.com');  -- несколько

-- UPDATE — изменить существующие:
UPDATE orders SET status = 'shipped' WHERE id = 10;        -- ⚠️ БЕЗ WHERE обновит ВСЕ строки!

-- DELETE — удалить:
DELETE FROM orders WHERE status = 'cancelled';             -- ⚠️ БЕЗ WHERE удалит ВСЁ!
```

💡 ⭐ **Самое опасное в SQL: UPDATE/DELETE без WHERE** изменяет/удаляет ВСЕ строки таблицы. Всегда
проверяй WHERE! Совет: сначала сделай `SELECT` с тем же WHERE (увидеть, какие строки затронутся),
потом меняй на UPDATE/DELETE. В транзакции можно откатить (модуль 16), но привычка проверять WHERE
спасает от катастроф.

---

## ⭐ DDL: управление структурой

```sql
-- CREATE — создать таблицу/индекс/etc:
CREATE TABLE products (id SERIAL PRIMARY KEY, name TEXT NOT NULL, price DECIMAL(10,2));

-- ALTER — изменить существующую таблицу:
ALTER TABLE products ADD COLUMN category_id INTEGER REFERENCES categories(id);  -- добавить столбец
ALTER TABLE products ALTER COLUMN price SET NOT NULL;                            -- изменить
ALTER TABLE products DROP COLUMN old_field;                                      -- удалить столбец

-- DROP — удалить объект целиком:
DROP TABLE products;        -- ⚠️ удаляет таблицу И ВСЕ данные! необратимо.

-- TRUNCATE — быстро очистить таблицу (все строки, структура остаётся):
TRUNCATE TABLE logs;        -- ⚠️ быстрее DELETE, но без WHERE и обычно без отката.
```

```
   DDL (Data Definition Language) — структура: CREATE, ALTER, DROP, TRUNCATE.
   DML (Data Manipulation Language) — данные: INSERT, UPDATE, DELETE, SELECT.
```

💡 ⭐ ALTER TABLE на работающей БД с данными — деликатно (модуль 22 «миграции»): добавить
обязательный столбец в большую таблицу, изменить тип — может блокировать/ломать. DROP/TRUNCATE
необратимы (без бэкапа) — будь предельно осторожен на production.

---

## ⭐⭐ RETURNING, UPSERT и безопасность

```sql
-- RETURNING (Postgres) — вернуть данные изменённых строк (удобно для id новой записи):
INSERT INTO clients (name) VALUES ('Анна') RETURNING id;   -- сразу получить сгенерированный id

-- UPSERT — вставить или обновить, если уже есть (ON CONFLICT):
INSERT INTO settings (key, value) VALUES ('theme', 'dark')
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;     -- есть key → обновить, нет → вставить

-- ⚠️ БЕЗОПАСНОСТЬ: в приложении НИКОГДА не склеивай данные в SQL строкой:
-- ❌ "INSERT ... VALUES ('" + name + "')"  → SQL-инъекция!
-- ✅ параметризованный запрос: VALUES (?) с передачей name отдельно (модуль безопасности).
```

💡 ⭐⭐ Критично: **в коде приложения используй ПАРАМЕТРИЗОВАННЫЕ запросы**, а не склейку строк с
пользовательским вводом — иначе SQL-инъекция (атакующий внедрит свой SQL). Это [уязвимость №3 OWASP](../../Security/02-vulnerabilities/09-injection-sqli.md).
`RETURNING` удобен для получения id новых записей; `ON CONFLICT` (upsert) — «вставь или обнови».

---

## 📖 Транзакции (превью Уровня 3)

```sql
-- группа изменений как ЕДИНОЕ ЦЕЛОЕ (всё или ничего):
BEGIN;
   UPDATE accounts SET balance = balance - 100 WHERE id = 1;   -- списать
   UPDATE accounts SET balance = balance + 100 WHERE id = 2;   -- зачислить
COMMIT;    -- зафиксировать обе. (или ROLLBACK — отменить обе, если что-то не так)
-- сбой посреди → откат → деньги не пропадут. подробно — модуль 16.
```

> 🧭 Безопасность данных: [параметризация против инъекций](../../Security/03-defensive-code/16-input-validation.md),
> доступ только нужный (наименьшие привилегии для пользователя БД приложения).

---

## ⚠️ Ловушки

- ❌ UPDATE/DELETE без WHERE → изменение/удаление ВСЕХ строк. КАТАСТРОФА.
- ❌ Склейка пользовательского ввода в SQL-строку → SQL-инъекция (используй параметры!).
- ❌ DROP/TRUNCATE без бэкапа на production (необратимо).
- ❌ ALTER большой таблицы без понимания блокировок (может «положить» БД).
- ❌ INSERT без указания столбцов (хрупко при изменении схемы) — перечисляй явно.
- ❌ Забыть, что изменения вне транзакции применяются сразу (нет отката).

---

## ✅ Задачи (на учебной базе)

1. **CRUD.** Вставь, обнови (с WHERE!), удали строки. Проверь результат SELECT после каждого.
2. **Безопасный UPDATE.** Перед UPDATE сделай SELECT с тем же WHERE — увидь затрагиваемые строки.
3. ⭐ **DDL.** Создай таблицу, добавь столбец (ALTER ADD), измени ограничение, удали столбец.
4. ⭐ **UPSERT + RETURNING.** Вставь с ON CONFLICT (upsert); получи id через RETURNING.
5. **Транзакция.** Сделай два связанных UPDATE в BEGIN...COMMIT; попробуй ROLLBACK — изменения отменились?

---

## ❓ Проверь себя

1. Что делают INSERT/UPDATE/DELETE и чем опасны без WHERE?
2. Что такое DDL (CREATE/ALTER/DROP/TRUNCATE) и его опасности?
3. Почему в приложении нужны параметризованные запросы?
4. Что такое UPSERT (ON CONFLICT) и RETURNING?

---

## ✅ Чек-лист

- [ ] Делаю INSERT/UPDATE/DELETE (всегда с WHERE!)
- [ ] Управляю структурой через DDL (CREATE/ALTER/DROP)
- [ ] Использую параметризацию против SQL-инъекций
- [ ] Применяю UPSERT и RETURNING
- [ ] Понимаю опасность операций без WHERE / на production

➡️ Дальше: [✅ Задачи уровня 2](TASKS.md) · [🚀 Проект](PROJECT.md) · затем
[Уровень 3 · Производительность](../03-performance/13-indexes.md)
