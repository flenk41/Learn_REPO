# 09 · Объекты из кода ⭐⭐ 🖼️

> 🎯 **Цель блока:** управлять миром из скриптов — находить объекты, менять их свойства, создавать и
> удалять. Это превращает статичную сцену в живую игру. Ядро скриптинга.

---

## ⭐⭐ Доступ к объектам дерева

```lua
   -- из кода ты ходишь по тому же дереву (game), что видишь в Explorer (модуль 04).
   local platform = workspace.Platform          -- workspace == game.Workspace
   local coin = game.Workspace.Coin.Handle       -- путь через точки

   -- безопаснее (объект мог не загрузиться):
   local platform = workspace:WaitForChild("Platform")    -- дождаться появления
   local maybe = workspace:FindFirstChild("Coin")         -- nil, если нет (без ошибки)

   -- сервисы — через GetService (модуль 11):
   local Players = game:GetService("Players")
```

💡 ⭐⭐ `workspace.Platform` из кода — это тот же объект, что в Explorer. **`:WaitForChild("имя")`** —
важнейшая привычка: объекты загружаются не мгновенно, и прямой `workspace.Platform` может упасть с
«Platform is not a valid member», если он ещё не появился. Для того, что может отсутствовать, —
`:FindFirstChild` (вернёт `nil` вместо ошибки).

---

## ⭐⭐ Чтение и изменение свойств

```lua
   local part = workspace.Platform

   -- читать
   print(part.Name)                  -- "Platform"
   print(part.Position)              -- Vector3

   -- менять (мир меняется мгновенно!)
   part.Transparency = 0.5
   part.Color = Color3.fromRGB(255, 0, 0)        -- красный
   part.Material = Enum.Material.Neon            -- материалы — через Enum
   part.Size = Vector3.new(10, 1, 10)
   part.Anchored = true
   part.CanCollide = false
```

🖼️
```
   код  ──меняет свойство──►  объект в Workspace  ──►  мир на экране меняется
   part.Color = красный   →   Platform краснеет   →   игрок видит красную платформу

   те же свойства, что в панели Properties, — но из скрипта и динамически (по событию, в цикле).
```

💡 ⭐⭐ Свойства из кода — это панель Properties, но **динамическая**: меняешь по событию или в цикле.
Цвета — через `Color3.fromRGB(r,g,b)`, размеры/позиции — `Vector3.new(x,y,z)`, материалы и прочие
наборы значений — через `Enum.Material.Neon` и т.п. (Enum = перечисление допустимых значений).

---

## ⭐⭐ Создание и удаление объектов

```lua
   -- СОЗДАТЬ объект из кода:
   local coin = Instance.new("Part")             -- создать Part (пока без родителя — нигде)
   coin.Name = "Coin"
   coin.Size = Vector3.new(2, 2, 2)
   coin.Material = Enum.Material.Neon
   coin.Color = Color3.fromRGB(255, 215, 0)      -- золотой
   coin.Anchored = true
   coin.Position = Vector3.new(0, 5, 0)
   coin.Parent = workspace                        -- ВАЖНО: появится в мире ТОЛЬКО задав Parent!

   -- УДАЛИТЬ:
   coin:Destroy()                                 -- убрать объект из игры полностью
```

💡 ⭐⭐ `Instance.new("Part")` создаёт объект, но он **появится в мире только когда задашь `.Parent`**
(пока Parent = nil — он нигде). Совет: настрой все свойства, и `.Parent = workspace` ставь
**последним** (иначе игрок на миг увидит недонастроенный объект). `:Destroy()` — удалить (например,
собранную монету). Так в симуляторе спавнятся и исчезают ресурсы.

---

## 📖 Клонирование

```lua
   -- размножить заготовку (например, монеты по карте):
   local template = game.ReplicatedStorage:WaitForChild("Coin")   -- заготовка в хранилище
   for i = 1, 10 do
       local c = template:Clone()                 -- копия
       c.Position = Vector3.new(i * 5, 5, 0)
       c.Parent = workspace
   end
```

💡 Частый приём: держать «заготовку» (в ReplicatedStorage/ServerStorage) и `:Clone()` её много раз —
так спавнят монеты, врагов, предметы, не создавая каждый вручную.

---

## ⚠️ Ловушки

- ❌ Обратиться к объекту до загрузки (`workspace.X`) → ошибка; используй `:WaitForChild`.
- ❌ Создать `Instance.new` и забыть `.Parent` → объект не появится (он нигде).
- ❌ Задать Parent ПЕРВЫМ, до настройки свойств → мигание недонастроенного объекта.
- ❌ Цвет числом вместо `Color3.fromRGB`, материал строкой вместо `Enum.Material.X`.
- ❌ Забывать `:Destroy()` для временных объектов → утечка (накапливаются, тормозят).

---

## ✅ Задачи

1. Скриптом измени цвет/материал/прозрачность своей платформы. Проверь в Play.
2. Создай монету `Instance.new("Part")` (Neon, золотая, Anchored), помести в workspace.
3. Поэкспериментируй: задай Parent ПЕРВЫМ vs ПОСЛЕДНИМ — заметна ли разница?
4. ⭐ Сделай заготовку Coin в ReplicatedStorage и наспавни 10 копий `:Clone()` в ряд.
5. ⭐ Создай монету, через 3 секунды удали её (`task.wait(3)` + `:Destroy()`).

---

## ❓ Проверь себя

1. Как из кода получить объект из Workspace и почему важен `:WaitForChild`?
2. Как читать и менять свойства (Color3/Vector3/Enum)?
3. Что делает `Instance.new` и почему нужен `.Parent`?
4. Зачем `:Clone()` и `:Destroy()`?

---

## ✅ Чек-лист

- [ ] Достаю объекты из дерева (`workspace.X`, `:WaitForChild`, `:FindFirstChild`)
- [ ] Читаю и меняю свойства (Color3/Vector3/Enum)
- [ ] Создаю объекты (`Instance.new` + `.Parent` последним) и удаляю (`:Destroy`)
- [ ] Размножаю заготовки через `:Clone()`

➡️ Следующий: [10 · События (Events) ⭐⭐](10-events.md)
