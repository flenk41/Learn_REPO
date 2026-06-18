# 12b · Шпаргалка кода: готовые рецепты 🖼️⭐⭐

> 🎯 **Цель блока:** справочник копируемых рецептов на Luau — «хочу сделать X → вот код». Держи под
> рукой, пока пишешь свою игру. Каждый рецепт помечен, **куда класть скрипт**.

> 🧭 Это практический сборник по модулям 08–17. Если рецепт непонятен — открой соответствующий модуль.
> Пиши код в **Script** (сервер, в `ServerScriptService`) или **LocalScript** (клиент) — указано у каждого.

---

## 📖 Памятка: куда класть скрипт

```
   Script (сервер)        → ServerScriptService   — логика, очки, данные, сохранение.
   LocalScript (клиент)   → StarterPlayerScripts / внутрь GUI — интерфейс, ввод, эффекты.
   ModuleScript (общий)   → ReplicatedStorage      — переиспользуемые функции.
   запускай ▶ Play, читай Output (View → Output): там print() и ошибки.
```

---

## 🟢 Базовое

**Вывести текст / отладка** · _Script_
```lua
print("Привет, Roblox!")          -- обычный вывод
warn("Что-то пошло не так")        -- предупреждение (жёлтым)
print("Очки:", 10, "игрок:", "Аня")  -- можно много значений через запятую
```

**Найти объект в мире** · _Script_
```lua
local part = workspace:WaitForChild("Coin")     -- дождаться (безопасно)
local maybe = workspace:FindFirstChild("Door")   -- nil, если нет (без ошибки)
local players = game:GetService("Players")        -- сервис
```

**Создать / удалить / копировать объект** · _Script_
```lua
local p = Instance.new("Part")
p.Size = Vector3.new(4, 1, 4)
p.Position = Vector3.new(0, 10, 0)
p.Color = Color3.fromRGB(255, 215, 0)   -- золотой
p.Material = Enum.Material.Neon
p.Anchored = true
p.Parent = workspace                     -- Parent ПОСЛЕДНИМ — иначе не появится!

p:Destroy()                              -- удалить

local copy = p:Clone()                   -- копия (не забудь задать .Parent)
copy.Parent = workspace
```

**Изменить свойства** · _Script_
```lua
local part = workspace.Platform
part.Transparency = 0.5
part.Color = Color3.fromRGB(255, 0, 0)
part.Material = Enum.Material.Wood
part.CanCollide = false
```

---

## 🔴 События (реакция на действия)

**Игрок коснулся детали (собрать монету)** · _Script_
```lua
local coin = workspace:WaitForChild("Coin")
local debounce = false

coin.Touched:Connect(function(otherPart)
    if debounce then return end                 -- защита от повторов
    local hum = otherPart.Parent:FindFirstChildWhichIsA("Humanoid")
    if hum then                                 -- коснулся именно игрок
        debounce = true
        print("Монета собрана!")
        coin:Destroy()
    end
end)
```

**Лава/урон при касании** · _Script_
```lua
local lava = workspace:WaitForChild("Lava")
lava.Touched:Connect(function(hit)
    local hum = hit.Parent:FindFirstChildWhichIsA("Humanoid")
    if hum then
        hum.Health = hum.Health - 20            -- нанести урон
    end
end)
```

**Кнопка-Part: при касании что-то происходит** · _Script_
```lua
local button = workspace:WaitForChild("Button")
local door = workspace:WaitForChild("Door")
local debounce = false

button.Touched:Connect(function(hit)
    if debounce then return end
    if hit.Parent:FindFirstChildWhichIsA("Humanoid") then
        debounce = true
        door.CanCollide = false
        door.Transparency = 0.7                 -- «открыть» дверь
        task.wait(2)
        door.CanCollide = true
        door.Transparency = 0
        debounce = false
    end
end)
```

---

## 👤 Игроки и очки

**Когда игрок заходит + создать счётчик (leaderstats)** · _Script_
```lua
local Players = game:GetService("Players")

Players.PlayerAdded:Connect(function(player)
    local stats = Instance.new("Folder")
    stats.Name = "leaderstats"           -- имя ОБЯЗАНО быть таким!
    stats.Parent = player

    local coins = Instance.new("IntValue")
    coins.Name = "Coins"
    coins.Value = 0
    coins.Parent = stats                 -- теперь "Coins" видно в таблице (Tab)
end)
```

**Дать очки игроку** · _Script_
```lua
local function addCoins(player, amount)
    local coins = player.leaderstats.Coins
    coins.Value = coins.Value + amount
end
-- пример: addCoins(player, 5)
```

**Найти игрока по его телу (в Touched)** · _Script_
```lua
local Players = game:GetService("Players")
-- внутри Touched, где otherPart — часть тела:
local player = Players:GetPlayerFromCharacter(otherPart.Parent)
if player then
    -- это игрок player
end
```

---

## ⏱️ Время, циклы, движение

**Подождать / обратный отсчёт** · _Script_
```lua
task.wait(3)                              -- пауза 3 секунды (не wait!)

for t = 10, 0, -1 do                      -- 10, 9, ... 0
    print("осталось " .. t)
    task.wait(1)
end
print("Время вышло!")
```

**Спавнить монеты по таймеру** · _Script_
```lua
local template = game.ReplicatedStorage:WaitForChild("Coin")  -- заготовка

while true do
    local c = template:Clone()
    c.Position = Vector3.new(math.random(-20, 20), 5, math.random(-20, 20))
    c.Parent = workspace
    task.wait(2)                          -- новая монета каждые 2 сек
end
```

**Плавно подвинуть объект (дверь вверх)** · _Script_
```lua
local TweenService = game:GetService("TweenService")
local door = workspace:WaitForChild("Door")

local info = TweenInfo.new(1)             -- 1 секунда
local goal = { Position = door.Position + Vector3.new(0, 10, 0) }
TweenService:Create(door, info, goal):Play()
```

**Ускорить игрока** · _Script_
```lua
local function speedUp(player, speed)
    local char = player.Character
    local hum = char and char:FindFirstChildWhichIsA("Humanoid")
    if hum then hum.WalkSpeed = speed end  -- обычная скорость = 16
end
```

---

## 🖥️ Интерфейс (GUI)

**Обновить текст на экране** · _LocalScript внутри ScreenGui_
```lua
local label = script.Parent:WaitForChild("CoinLabel")  -- TextLabel
label.Text = "💰 0"

-- обновлять при изменении валюты:
local player = game.Players.LocalPlayer
local coins = player:WaitForChild("leaderstats"):WaitForChild("Coins")
coins.Changed:Connect(function(newValue)
    label.Text = "💰 " .. newValue
end)
```

**Нажатие кнопки** · _LocalScript внутри ScreenGui_
```lua
local button = script.Parent:WaitForChild("BuyButton")  -- TextButton
button.MouseButton1Click:Connect(function()
    print("Кнопка нажата!")
    -- ВАЖНО: саму покупку делает СЕРВЕР (см. RemoteEvent ниже)
end)
```

---

## 🔗 Клиент ↔ сервер (RemoteEvent)

> Сначала вставь **RemoteEvent** в `ReplicatedStorage`, назови `BuyUpgrade`.

**Клиент просит** · _LocalScript_
```lua
local remote = game.ReplicatedStorage:WaitForChild("BuyUpgrade")
button.MouseButton1Click:Connect(function()
    remote:FireServer("speed")            -- попросить сервер. игрока НЕ передаём!
end)
```

**Сервер проверяет и делает** · _Script_
```lua
local remote = game.ReplicatedStorage:WaitForChild("BuyUpgrade")

remote.OnServerEvent:Connect(function(player, kind)   -- player подставит Roblox сам
    local cost = 100                                  -- цену знает СЕРВЕР
    local coins = player.leaderstats.Coins
    if coins.Value >= cost then                       -- ПРОВЕРКА!
        coins.Value = coins.Value - cost
        speedUp(player, 32)                           -- выдать апгрейд
    end
end)
```

---

## 💾 Сохранение прогресса (DataStore)

> Включи: Game Settings → Security → **Enable Studio Access to API Services**. Работает в опубликованной игре.

· _Script_
```lua
local DataStoreService = game:GetService("DataStoreService")
local Players = game:GetService("Players")
local store = DataStoreService:GetDataStore("PlayerData")

Players.PlayerAdded:Connect(function(player)
    -- создать leaderstats (см. выше) ...
    local key = "Player_" .. player.UserId
    local ok, data = pcall(function()
        return store:GetAsync(key)
    end)
    if ok and data then
        player.leaderstats.Coins.Value = data         -- загрузить
    end
end)

Players.PlayerRemoving:Connect(function(player)
    local key = "Player_" .. player.UserId
    pcall(function()
        store:SetAsync(key, player.leaderstats.Coins.Value)  -- сохранить
    end)
end)
```

---

## 🧩 Общий код (ModuleScript)

**ModuleScript** в `ReplicatedStorage`, имя `GameUtils`:
```lua
local GameUtils = {}

function GameUtils.format(n)
    return tostring(n) .. " монет"
end

return GameUtils                          -- модуль ВОЗВРАЩАЕТ таблицу
```
**Использование** · _любой Script/LocalScript_
```lua
local GameUtils = require(game.ReplicatedStorage:WaitForChild("GameUtils"))
print(GameUtils.format(50))               -- "50 монет"
```

---

## ⚠️ Частые ошибки (читай Output!)

```
   "X is not a valid member of Workspace"  → объект ещё не загрузился → используй :WaitForChild("X").
   "attempt to index nil"                  → обращаешься к тому, чего нет (опечатка в имени / objects nil).
   Часть падает при Play                   → забыл Anchored = true.
   Монета даёт очки 10 раз                 → нет debounce (Touched стреляет пачкой).
   Покупка «бесплатна» у читера            → выдаёшь на клиенте; делай на СЕРВЕРЕ с проверкой.
   leaderstats не виден в Tab              → папка названа не ровно "leaderstats".
   wait() работает странно                 → используй task.wait().
```

💡 ⭐⭐ Главное правило отладки: **держи Output открытым и читай текст ошибки** — он почти всегда
говорит, ЧТО и ГДЕ не так (имя объекта, номер строки). 90% проблем новичка — забытый `:WaitForChild`,
забытый `Anchored`, отсутствие debounce или логика на клиенте вместо сервера.

---

## ✅ Как пользоваться шпаргалкой

1. Нашёл нужный рецепт → скопировал в скрипт нужного типа (Script/LocalScript) → поменял имена объектов под свои.
2. ▶ Play → проверил в Output.
3. Не работает → прочитал ошибку → нашёл её в списке выше или открыл нужный модуль.

➡️ Назад к уроку: [✅ Задачи уровня 2](TASKS.md) · 🚀 [Проект: ядро симулятора](PROJECT.md) · далее [🦅 Уровень 3](../03-gameplay/13-movement-physics.md)
