# 17b · Сделай свою механику + оптимизация (step-by-step) 🖼️⭐⭐

> 🎯 **Цель блока:** дать пошаговый метод, по которому ты сам придумаешь и закодишь ЛЮБУЮ механику —
> и оптимизируешь её, как делают настоящие разработчики. Разбираем на примере **лазания с зацепом
> ЛКМ/ПКМ** (как в играх про подъём в горы).

> 🧭 Опирается на события (модуль 10), сервисы/ввод (11), физику (13), клиент-сервер (15). Это
> методология — она переносится на любую механику (двойной прыжок, грэпплинг-крюк, паркур, стрельба).

---

## ⭐⭐ Метод из 7 шагов (работает для любой механики)

```
   1. ОПИШИ СЛОВАМИ — что игрок делает, что чувствует, по каким правилам. одно-два предложения.
   2. РАЗБЕЙ НА ЧАСТИ — ВВОД → СОСТОЯНИЕ → ЛОГИКА → ФИЗИКА/ДВИЖЕНИЕ → ОБРАТНАЯ СВЯЗЬ.
   3. ОПРЕДЕЛИ СОСТОЯНИЕ — какие переменные описывают механику «сейчас»?
   4. ПОЙМАЙ ВВОД — какие кнопки/события и как их слушать.
   5. НАПИШИ ЯДРО — самое простое работающее правило (без красоты).
   6. ДОБАВЬ ФИЗИКУ/ОБРАТНУЮ СВЯЗЬ — движение тела, визуал, звук.
   7. ИТЕРИРУЙ И ЧИНИ — тестируй, лови баги, настраивай «на ощупь».
```

💡 ⭐⭐ Главное: **не пиши механику сразу целиком**. Разбей на ВВОД → СОСТОЯНИЕ → ЛОГИКА →
ФИЗИКА → ОБРАТНАЯ СВЯЗЬ и собери по кусочку, проверяя каждый. Так делается любая механика — от
двойного прыжка до зацепа. Сложное = много простых проверяемых частей.

---

## 🧗 Шаг 1 — Опиши механику словами

```
   ЛАЗАНИЕ С ЗАЦЕПОМ:
   • держу ЛКМ → ЛЕВАЯ рука цепляется за поверхность в точке прицела; отпустил ЛКМ → рука отпускает.
   • держу ПКМ → то же для ПРАВОЙ руки.
   • пока хоть одна рука держится — тело висит/подтягивается к зацепу (не падает).
   • поднимаюсь, чередуя руки: зацепился выше одной → отпустил и перецепил другую выше.
   • обе руки отпущены → падаю.
   ощущение: напряжённый, «ручной» подъём, где важен каждый зацеп.
```

💡 Запиши так ЛЮБУЮ свою механику до кода. Это твоё ТЗ: пока не можешь описать словами — кодить рано.

---

## 🧩 Шаг 2-3 — Разбей и определи состояние

```
   разбивка лазания:
   • ВВОД — ЛКМ/ПКМ нажата/отпущена.
   • СОСТОЯНИЕ — какая рука где держится.
   • ЛОГИКА — при нажатии найти точку зацепа (луч от прицела к поверхности).
   • ФИЗИКА — пока держимся, тянуть тело к зацепам, выключить обычное падение.
   • ОБРАТНАЯ СВЯЗЬ — линия/рука к зацепу, звук.
```

**Состояние** (в LocalScript игрока — персонаж управляется клиентом):
```lua
local grips = {
    Left  = nil,   -- Vector3 точки зацепа левой руки (или nil)
    Right = nil,   -- то же для правой
}
local REACH = 12   -- максимальная дальность зацепа (изучай/настраивай)
```

---

## 🖱️ Шаг 4 — Поймай ввод (ЛКМ/ПКМ в мире)

> Клики по миру (не по GUI) ловят через **UserInputService** в **LocalScript**
> (`StarterPlayerScripts`).

```lua
local UserInputService = game:GetService("UserInputService")

UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end                      -- клик был по UI — игнор
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        tryGrab("Left")
    elseif input.UserInputType == Enum.UserInputType.MouseButton2 then
        tryGrab("Right")
    end
end)

UserInputService.InputEnded:Connect(function(input)
    if input.UserInputType == Enum.UserInputType.MouseButton1 then
        release("Left")
    elseif input.UserInputType == Enum.UserInputType.MouseButton2 then
        release("Right")
    end
end)
```

💡 ⭐ `InputBegan`/`InputEnded` + проверка `UserInputType` — стандарт для мышиного/клавиатурного ввода
в мире. `gameProcessed` отсекает клики, которые «съел» интерфейс (чтобы клик по кнопке не цеплялся).

---

## 🎯 Шаг 5 — Ядро: найти точку зацепа (raycast)

```lua
local Players = game:GetService("Players")
local player = Players.LocalPlayer
local camera = workspace.CurrentCamera

local function tryGrab(hand)
    local character = player.Character
    if not character then return end
    local root = character:FindFirstChild("HumanoidRootPart")
    if not root then return end

    -- луч от камеры через позицию мыши:
    local mousePos = UserInputService:GetMouseLocation()
    local ray = camera:ViewportPointToRay(mousePos.X, mousePos.Y)

    local params = RaycastParams.new()
    params.FilterType = Enum.RaycastFilterType.Exclude
    params.FilterDescendantsInstances = { character }     -- не цепляться за себя

    local result = workspace:Raycast(ray.Origin, ray.Direction * 100, params)
    if result then
        local hitPart = result.Instance
        local point = result.Position
        -- цепляемся только за помеченные «Climbable» и в пределах REACH:
        if hitPart:GetAttribute("Climbable") and (point - root.Position).Magnitude <= REACH then
            grips[hand] = point                           -- ЗАПОМНИЛИ точку зацепа
        end
    end
end

local function release(hand)
    grips[hand] = nil
end
```

💡 ⭐⭐ Ядро механики — **raycast** (луч): «куда смотрит игрок → есть ли там за что зацепиться?».
`workspace:Raycast(origin, direction, params)` возвращает точку и объект попадания. Помечай
лазаемые поверхности атрибутом `Climbable = true` (Properties → Attributes) — так механика работает
только где задумано, а не «за воздух».

---

## 🪢 Шаг 6 — Физика: подтянуть тело к зацепам

> Идея: пока держится ≥1 рука — выключаем обычное падение и **тянем тело** к зацепам силой.
> Используем `AlignPosition` (констрейнт, плавно подтягивающий объект к цели).

```lua
local RunService = game:GetService("RunService")

-- один раз настроить тягу на HumanoidRootPart:
local function setupPull(root)
    local att = Instance.new("Attachment", root)
    local align = Instance.new("AlignPosition")
    align.Attachment0 = att
    align.Mode = Enum.AlignPositionMode.OneAttachment    -- тянуть к МИРОВОЙ позиции
    align.MaxForce = 60000
    align.Responsiveness = 30
    align.Enabled = false
    align.Parent = root
    return align
end

-- каждый кадр обновляем цель тяги:
RunService.RenderStepped:Connect(function()
    local character = player.Character
    local root = character and character:FindFirstChild("HumanoidRootPart")
    local hum = character and character:FindFirstChildWhichIsA("Humanoid")
    if not (root and hum) then return end

    local active = {}
    if grips.Left  then table.insert(active, grips.Left)  end
    if grips.Right then table.insert(active, grips.Right) end

    if #active > 0 then
        hum.PlatformStand = true                          -- выключить обычную ходьбу/падение → висим
        -- цель = средняя точка зацепов, чуть ниже (тело висит под руками):
        local target = Vector3.zero
        for _, p in ipairs(active) do target += p end
        target = target / #active - Vector3.new(0, 3, 0)
        align.Position = target
        align.Enabled = true
    else
        hum.PlatformStand = false                         -- отпустил обе → падаешь
        align.Enabled = false
    end
end)
```

💡 ⭐⭐ Это **упрощённая, но рабочая** модель: тело притягивается к зацепам, `PlatformStand = true`
отключает обычную локомоцию (персонаж «висит»). Чередуя ЛКМ/ПКМ и цепляясь выше — поднимаешься.
Для «настоящей» физики (раскачка, вес, инерция рук) берут связку констрейнтов
(`BallSocketConstraint`/`RopeConstraint` на руки + `AlignOrientation`) — но начни с простого и почувствуй,
потом усложняй. **Сначала «работает», потом «реалистично».**

---

## ✨ Шаг 7 — Обратная связь и итерация

```
   обратная связь (чтобы механика «читалась»):
   • визуал — рисуй линию/Beam от руки к точке зацепа (видно, что держишься).
   • звук — щелчок при зацепе, кряхтение при подтягивании.
   • камера/тряска — лёгкий эффект усилия.

   итерация (настройка «на ощупь»):
   • крути REACH, MaxForce, Responsiveness, offset — пока не станет приятно.
   • тестируй краевые случаи: зацеп за край, обе руки сразу, потеря персонажа (респаун).
   • показывай другим — со стороны видно, что непонятно.
```

💡 Механика рождается в **итерациях**: первая версия всегда «деревянная», играбельной её делает
настройка чисел и обратная связь. Это нормально — закладывай время на «поиграть и подкрутить».

---

## ⚡ Оптимизация — как делают разработчики

> Механика на `RenderStepped`/`Heartbeat` работает каждый кадр — здесь легко уронить FPS. Вот приёмы профи.

```
   1. ИЗМЕРЯЙ, НЕ УГАДЫВАЙ — Developer Console (F9), MicroProfiler (Ctrl+F6). сначала найди, ГДЕ горячо.
   2. НЕ ДЕЛАЙ ЛИШНЕГО КАЖДЫЙ КАДР:
      • raycast — только при НАЖАТИИ (событие), а не каждый кадр. (у нас уже так — в tryGrab.)
      • тяжёлые вычисления — кэшируй результат, обновляй реже.
   3. КЭШИРУЙ ССЫЛКИ — не вызывай :FindFirstChild/:GetService в цикле; достань один раз, храни в переменной.
   4. РАННИЙ ВЫХОД (guard) — `if not root then return end` в начале: не считать, если нечего.
   5. THROTTLE — что не обязано быть каждый кадр, делай раз в N кадров/по таймеру (напр. проверка
      окружения раз в 0.1с, а не 60 раз/сек).
   6. ПУЛ ОБЪЕКТОВ — не Instance.new/Destroy в горячем цикле (Beam, эффекты); создай раз, переиспользуй.
   7. ОТПИСЫВАЙСЯ от событий и :Destroy() ненужное (иначе утечки копятся).
   8. МИНИМИЗИРУЙ СЕТЬ — не шли RemoteEvent каждый кадр; шли итог/реже (модуль 19/20).
```

🖼️
```
   дёшево (по событию):              дорого (каждый кадр):
   raycast при клике ✅              raycast 60 раз/сек ❌
   кэш root в переменной ✅          root = char:FindFirstChild(...) в цикле ❌
   проверка раз в 0.1с ✅            тяжёлая проверка каждый кадр ❌
```

💡 ⭐⭐ Золотое правило оптимизации (то же, что у инженеров вне игр): **сначала измерь, потом
оптимизируй именно горячее место**. Самый частый выигрыш в механиках — убрать тяжёлое из покадрового
цикла (raycast/поиск/вычисления → по событию или реже) и кэшировать ссылки. Не оптимизируй вслепую —
[это потеря времени](../04-publish/20-optimization.md).

---

## ⚠️ Ловушки

- ❌ Кодить всю механику сразу, а не по частям (ввод→состояние→логика→физика→фидбек).
- ❌ Raycast/поиск объектов каждый кадр вместо «по событию» (убивает FPS).
- ❌ Вызывать `:GetService`/`:FindFirstChild` в покадровом цикле (кэшируй в переменную).
- ❌ Нет раннего выхода (`if not root then return end`) → ошибки при респауне/загрузке.
- ❌ Гнаться за «реализмом» до того, как механика просто заработала.
- ❌ Оптимизировать без измерения (чинишь не то).
- ❌ Не помечать поверхности (`Climbable`) → цепляешься «за воздух»/за что попало.

---

## ✅ Задачи

1. Опиши СЛОВАМИ свою механику (любую) по шаблону шага 1. Разбей на 5 частей (шаг 2).
2. Сделай минимальную версию зацепа: лови ЛКМ/ПКМ (`InputBegan`) и печатай, какая рука «цепляется».
3. Добавь raycast: при клике печатай, попал ли в `Climbable`-поверхность и на каком расстоянии.
4. ⭐ Подключи тягу (`AlignPosition` + `PlatformStand`) — повиси на одном зацепе. Покрути MaxForce/offset.
5. ⭐ Оптимизируй: убедись, что raycast только по клику, ссылки кэшированы, есть guard'ы. Замерь FPS (F9).
6. ⭐⭐ Перенеси метод на ДРУГУЮ механику (двойной прыжок / рывок-dash / грэпплинг). Те же 7 шагов.

---

## ❓ Проверь себя

1. Назови 5 частей, на которые разбивается любая механика.
2. Как поймать ЛКМ/ПКМ в мире (какой сервис и события)?
3. Зачем raycast и атрибут `Climbable`?
4. Какие приёмы оптимизации применяют к покадровой механике?
5. Почему «сначала работает, потом реалистично»?

---

## ✅ Чек-лист

- [ ] Проектирую механику по шагам (ввод→состояние→логика→физика→фидбек)
- [ ] Ловлю ввод через UserInputService, ищу зацеп через raycast
- [ ] Двигаю тело констрейнтами (AlignPosition/PlatformStand), итерирую числа
- [ ] Оптимизирую по приборам: тяжёлое — по событию/реже, ссылки кэширую, guard'ы
- [ ] Умею перенести метод на любую новую механику

➡️ Назад к уроку: [🚀 Уровень 4 · Доводка](../04-publish/18-multiplayer-replication.md) · шпаргалка кода: [12b](../02-scripting/12b-code-cookbook.md)
