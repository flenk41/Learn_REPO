# 🚀 Пет-проект уровня 3 — Текстовый квест на ООП

> 🎯 **Цель:** собрать всё из Middle — классы, наследование, полиморфизм, шаблоны, STL,
> умные указатели — в одну ООП-программу с понятной архитектурой.

---

## 📋 Что делаем

Текстовую игру-инвентарь / мини-РПГ: игрок ходит по комнатам, собирает предметы, сражается.
Или, проще — **система инвентаря с предметами разных типов** (полиморфизм).

```
=== ИНВЕНТАРЬ ===
1. Меч (урон: 10, вес: 3.0)
2. Зелье лечения (+20 HP, вес: 0.5)
3. Щит (защита: 5, вес: 4.0)
Общий вес: 7.5
Команды: use N / drop N / list / quit
> use 2
Выпил зелье лечения. HP: 100 → 120
```

---

## ✅ Требования (минимум)

- [ ] Абстрактный базовый класс `Item` с виртуальными методами (`describe()`, `use()`,
      `getWeight()`).
- [ ] Минимум 3 производных класса (`Weapon`, `Potion`, `Shield`) с `override`.
- [ ] **Виртуальный деструктор** в базовом классе.
- [ ] Инвентарь — `std::vector<std::unique_ptr<Item>>` (полиморфное владение).
- [ ] Использование STL-алгоритмов (например `accumulate` для общего веса).
- [ ] Инкапсуляция: поля приватные, доступ через методы.
- [ ] Команды: список, использовать, выбросить, выход.
- [ ] **Ноль утечек** под ASan.

---

## 🪜 Пошаговый план

1. **Базовый класс.** Абстрактный `Item` с чисто виртуальными методами и виртуальным
   деструктором.
2. **Потомки.** `Weapon`, `Potion`, `Shield` — каждый со своими полями и `override`.
3. **Инвентарь.** Класс `Inventory` с `vector<unique_ptr<Item>>`, методы add/remove/list.
4. **Полиморфизм.** Метод `listAll()` вызывает `describe()` каждого предмета — выводится
   нужная версия.
5. **STL.** Общий вес через `std::accumulate` с лямбдой.
6. **Игрок.** Класс `Player` с HP, инвентарём; `use(i)` применяет предмет.
7. **Цикл команд.** Чтение и обработка команд.
8. **ASan.** Чистый прогон (умные указатели → утечек быть не должно).

---

## 🧱 Скелет

```cpp
#include <iostream>
#include <vector>
#include <memory>
#include <numeric>
#include <string>

class Item {
public:
    virtual std::string describe() const = 0;   // чисто виртуальный
    virtual double getWeight() const = 0;
    virtual void use() = 0;
    virtual ~Item() = default;                   // виртуальный деструктор!
};

class Weapon : public Item {
    std::string name; int damage; double weight;
public:
    Weapon(std::string n, int d, double w) : name(std::move(n)), damage(d), weight(w) {}
    std::string describe() const override {
        return name + " (урон: " + std::to_string(damage) + ")";
    }
    double getWeight() const override { return weight; }
    void use() override { std::cout << "Атакуешь " << name << "!\n"; }
};

// реализуй Potion, Shield по аналогии

class Inventory {
    std::vector<std::unique_ptr<Item>> items;
public:
    void add(std::unique_ptr<Item> item) { items.push_back(std::move(item)); }

    void list() const {
        for (size_t i = 0; i < items.size(); ++i)
            std::cout << i + 1 << ". " << items[i]->describe() << "\n";
        std::cout << "Общий вес: " << totalWeight() << "\n";
    }

    double totalWeight() const {
        return std::accumulate(items.begin(), items.end(), 0.0,
            [](double sum, const auto& item){ return sum + item->getWeight(); });
    }
    // реализуй use(i), remove(i)
};

int main() {
    Inventory inv;
    inv.add(std::make_unique<Weapon>("Меч", 10, 3.0));
    // ... добавь другие предметы, сделай цикл команд
    inv.list();
    return 0;
}
```
```bash
g++ -std=c++17 -Wall -Wextra -fsanitize=address -g game.cpp -o game
```

---

## 💪 Усложнения (для «отлично»)

- ➕ Комнаты и перемещение между ними (граф на `map`).
- ➕ Сражения с врагами (полиморфные `Enemy`).
- ➕ Сохранение/загрузка инвентаря в файл.
- ➕ Шаблонный контейнер-обёртка вместо vector.
- ➕ Сортировка инвентаря по весу/имени через STL-алгоритмы.
- ➕ Разделение на `.h`/`.cpp` + CMake.

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | Полиморфная иерархия + unique_ptr + STL + команды, ASan чист |
| 🌟 Хорошо | + комнаты/враги/сохранение |
| 🏆 Отлично | + шаблоны, разбивка на файлы, аккуратная архитектура |

---

## 🎓 Чему ты научился

Ты построил настоящую ООП-программу с полиморфизмом и автоматическим управлением памятью
через умные указатели. Заметь: несмотря на динамическое создание десятков объектов, ты ни
разу не написал `delete` — RAII и `unique_ptr` сделали всё сами. Это и есть современный C++.

Сохрани в `my-code/Cpp/03-game/`. 🎉

➡️ Финальный рывок: [Уровень 4 · Senior](../04-senior/19-move-deep.md)
