# 🚀 Мини-проект — Библиотека-клиент веб-API с чистым API

> 🎯 **Цель:** собрать **настоящий Rust-проект** — крейт-библиотеку клиента для веб-сервиса
> с чистым API (модули, pub-видимость, типы ошибок, serde) плюс бинарь, который её
> использует. Объединяет обе грани: **используешь** чужой API и **проектируешь** свой.

---

## 📋 Что делаем

Крейт-библиотеку клиента (погода через open-meteo или GitHub), которой удобно пользоваться,
не зная про reqwest/serde внутри:

```rust
use weatherlib::WeatherClient;

let client = WeatherClient::new();
let weather = client.get_weather("Москва")?;
println!("{}: {}°C", weather.city, weather.temperature);
```

---

## 📂 Требуемая структура (workspace)

```
weatherlib/
├── Cargo.toml             ← workspace
├── core/                  ← крейт-библиотека (логика)
│   ├── Cargo.toml
│   └── src/
│       ├── lib.rs         ← публичный API (pub use ...)
│       ├── client.rs      ← WeatherClient (reqwest спрятан здесь)
│       ├── models.rs      ← struct Weather (serde)
│       └── error.rs       ← enum WeatherError
└── cli/                   ← крейт-программа
    ├── Cargo.toml
    └── src/main.rs        ← использует core
```

*(можно проще: один крейт с модулями `client`, `models`, `error` + `main.rs`.)*

---

## ✅ Требования (минимум)

- [ ] Крейт-библиотека (`lib.rs`) с модулями `client`, `models`, `error`.
- [ ] `WeatherClient` с чистым **pub** API; reqwest/serde скрыты в реализации.
- [ ] Результат — типизированная структура (`Weather`) через `#[derive(Deserialize)]`.
- [ ] **Свой тип ошибки** (`enum WeatherError` с `Display` + `Error`).
- [ ] Обработка ошибок через `Result`/`?` (сеть, парсинг, плохой код ответа).
- [ ] Ключи (если есть) — из переменных окружения.
- [ ] Тесты (`cargo test`), документация (`///`).
- [ ] `cargo clippy` чист.

---

## 🪜 Пошаговый план

1. **Проект.** `cargo new weatherlib --lib` (+ `cli` крейт или просто `main.rs`).
   Зависимости: `reqwest` (blocking, json), `serde` (derive).
2. **API-first.** Спроектируй `lib.rs`: что `pub` (модуль 2). `WeatherClient::new`,
   `get_weather(city) -> Result<Weather, WeatherError>`.
3. **Модели.** `models.rs` — `struct Weather` с `Deserialize`.
4. **Ошибки.** `error.rs` — `enum WeatherError` (сеть, парсинг, не найдено) + `Display`.
5. **Клиент.** `client.rs` — внутри reqwest, парсинг serde, преобразование ошибок.
   Наружу — только pub-методы.
6. **CLI.** `main.rs` — берёт город из `std::env::args`, зовёт клиент, печатает, обрабатывает
   ошибки.
7. **Тесты + doc.** Покрой логику тестами, добавь `///`-примеры.

---

## 🧱 Скелеты

**src/models.rs:**
```rust
use serde::Deserialize;

#[derive(Deserialize, Debug, Clone)]
pub struct Weather {
    pub city: String,
    pub temperature: f64,
    pub wind: f64,
}
```

**src/error.rs:**
```rust
#[derive(Debug)]
pub enum WeatherError {
    Network(reqwest::Error),
    NotFound,
}

impl std::fmt::Display for WeatherError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            WeatherError::Network(e) => write!(f, "ошибка сети: {}", e),
            WeatherError::NotFound => write!(f, "город не найден"),
        }
    }
}
impl std::error::Error for WeatherError {}

impl From<reqwest::Error> for WeatherError {     // для удобного ?
    fn from(e: reqwest::Error) -> Self { WeatherError::Network(e) }
}
```

**src/client.rs:**
```rust
use crate::models::Weather;
use crate::error::WeatherError;

pub struct WeatherClient {
    client: reqwest::blocking::Client,
}

impl WeatherClient {
    pub fn new() -> Self {
        WeatherClient { client: reqwest::blocking::Client::new() }
    }

    /// Получить погоду по городу.
    pub fn get_weather(&self, city: &str) -> Result<Weather, WeatherError> {
        // 1. геокодинг города → координаты
        // 2. запрос погоды по координатам
        // 3. распарсить в Weather (serde), вернуть
        // реализуй сам, используя self.client.get(...).send()?.json()?
        todo!()
    }
}
```

**src/lib.rs:**
```rust
mod client;
mod models;
mod error;

pub use client::WeatherClient;     // публичный API крейта
pub use models::Weather;
pub use error::WeatherError;
```

> 💡 `pub use` в `lib.rs` — это «фасад»: пользователь пишет `use weatherlib::WeatherClient`,
> не зная внутренней структуры модулей. Чистый API.

---

## 💪 Усложнения (для «отлично»)

- ➕ Async-версия (tokio + reqwest async).
- ➕ Прогноз на несколько дней (`Vec<Weather>`).
- ➕ Builder для клиента (таймаут, единицы измерения).
- ➕ Кэш ответов.
- ➕ Тесты с мок-сервером (`mockito`).
- ➕ Публикация на crates.io (или хотя бы `cargo package`).

---

## 🏆 Критерии готовности

| Уровень | Что сделано |
|---------|-------------|
| ✅ Зачёт | Библиотека с чистым pub API + serde-структуры + свой тип ошибки + обработка, clippy чист |
| 🌟 Хорошо | + тесты, документация, builder или прогноз |
| 🏆 Отлично | + async, мок-тесты, workspace, готовность к публикации |

---

## 🎓 Чему ты научился

Ты собрал полноценный Rust-крейт, который **использует чужой веб-API** и **предоставляет
свой чистый типобезопасный API** поверх него — с модулями, pub-фасадом, типами ошибок и
serde. Это типовая архитектура реальных Rust-библиотек и SDK.

Сохрани в `my-code/Rust/weatherlib/`. 🎉

➡️ Назад к [разделу](README.md) · [дорожной карте Rust](../README.md)
