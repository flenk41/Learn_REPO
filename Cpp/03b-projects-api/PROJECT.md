# 🚀 Мини-проект — Библиотека-клиент веб-API с чистым API

> 🎯 **Цель:** собрать **настоящий C++ проект** — библиотеку-клиент для веб-сервиса,
> оформленную через CMake, с чистым API (header/source, при желании pImpl), которая
> объединяет обе грани: **используешь** чужой API и **проектируешь** свой.

---

## 📋 Что делаем

Библиотеку-клиент (например для погоды через open-meteo или GitHub), которой удобно
пользоваться, не зная про cpr и json внутри:

```cpp
#include <weatherlib/client.hpp>

weatherlib::Client client;
weatherlib::Weather w = client.getWeather("Москва");
std::cout << w.city << ": " << w.temperature << "°C\n";
```

---

## 📂 Требуемая структура

```
weatherlib/
├── include/weatherlib/
│   ├── client.hpp        ← публичный API (класс Client)
│   └── weather.hpp       ← struct Weather, исключения
├── src/
│   └── client.cpp        ← реализация (cpr + json спрятаны здесь)
├── apps/
│   └── main.cpp          ← консольная программа использует библиотеку
├── tests/
│   └── test_client.cpp
├── CMakeLists.txt
└── README.md
```

---

## ✅ Требования (минимум)

- [ ] **CMake**-проект: библиотека (`add_library`) + программа (`add_executable`),
      зависимости (cpr, nlohmann/json) через `FetchContent`.
- [ ] Класс `Client` с чистым API: публичные методы, реализация (cpr/json) скрыта в `.cpp`.
- [ ] Результат — структура (`struct Weather`/`struct User`), а не сырой JSON.
- [ ] **Свои исключения** (`ApiError`, `NotFound`) вместо кодов/печати.
- [ ] Обработка ошибок: таймаут, плохой код ответа, битый JSON.
- [ ] const correctness, владение выражено типами.
- [ ] Ключи (если есть) — из переменных окружения.
- [ ] 2–3 теста.
- [ ] README с описанием API и сборкой.

---

## 🪜 Пошаговый план

1. **API-first.** Сначала спроектируй `client.hpp` и `weather.hpp` — какие методы и
   структуры нужны пользователю (модуль 2). Реализацию пока не думай.
2. **CMake.** Настрой проект с FetchContent для cpr и nlohmann/json.
3. **Реализация.** В `client.cpp` — запрос через cpr, парсинг json в `Weather`, обработка
   ошибок. cpr и json **не должны** появляться в заголовках.
4. **Программа.** `main.cpp` использует только `weatherlib/*.hpp`.
5. **Тесты.** Проверь парсинг и обработку ошибок.
6. **Полировка.** README, обработка кривого ввода.

---

## 🧱 Скелеты

**include/weatherlib/weather.hpp:**
```cpp
#pragma once
#include <string>
#include <stdexcept>

namespace weatherlib {

struct Weather {
    std::string city;
    double temperature;
    double wind;
    std::string description;
};

class ApiError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

}  // namespace weatherlib
```

**include/weatherlib/client.hpp:**
```cpp
#pragma once
#include <string>
#include "weatherlib/weather.hpp"

namespace weatherlib {

class Client {
public:
    explicit Client(int timeout_ms = 10000);

    /// Получить погоду по городу. Бросает ApiError при ошибке.
    Weather getWeather(const std::string& city) const;

private:
    int timeout_ms_;
    // cpr/json НЕ упоминаются здесь — они только в client.cpp
};

}  // namespace weatherlib
```

**CMakeLists.txt:**
```cmake
cmake_minimum_required(VERSION 3.15)
project(weatherlib CXX)
set(CMAKE_CXX_STANDARD 17)

include(FetchContent)
FetchContent_Declare(cpr GIT_REPOSITORY https://github.com/libcpr/cpr.git GIT_TAG 1.10.5)
FetchContent_Declare(json GIT_REPOSITORY https://github.com/nlohmann/json.git GIT_TAG v3.11.3)
FetchContent_MakeAvailable(cpr json)

add_library(weatherlib src/client.cpp)
target_include_directories(weatherlib PUBLIC include)
target_link_libraries(weatherlib PRIVATE cpr::cpr nlohmann_json::nlohmann_json)

add_executable(weather apps/main.cpp)
target_link_libraries(weather PRIVATE weatherlib)
```

`src/client.cpp` — реализуй сам: внутри `cpr::Get`, `json::parse`, преобразование в
`Weather`, бросание `ApiError` при проблемах.

---

## 💪 Усложнения (для «отлично»)

- ➕ pImpl: спрячь cpr/json-состояние полностью за `unique_ptr<Impl>`.
- ➕ Прогноз на несколько дней (`std::vector<Weather>`).
- ➕ Кэш ответов (избегать повторных запросов).
- ➕ `std::optional<Weather> tryGetWeather(...)` — версия без исключений.
- ➕ Тесты с мок-ответом (без реальной сети).
- ➕ Установка библиотеки (`install(TARGETS ...)`), `find_package`-совместимость.

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | CMake + библиотека с чистым API + структуры + исключения + обработка ошибок |
| 🌟 Хорошо | + тесты, кэш или прогноз, README |
| 🏆 Отлично | + pImpl, мок-тесты, install-совместимость |

---

## 🎓 Чему ты научился

Ты собрал полноценную C++ библиотеку, которая **использует чужой веб-API** и
**предоставляет свой чистый API** поверх него — с CMake, скрытой реализацией, структурами
и исключениями. Это типовая архитектура реальных C++ SDK и клиентских библиотек.

Сохрани в `my-code/Cpp/weatherlib/`. 🎉

➡️ Назад к [разделу](README.md) · [дорожной карте C++](../README.md)
