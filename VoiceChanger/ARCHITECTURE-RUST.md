# 🦀 Voice Changer — архитектура на Rust

> Стек Rust: безопасность памяти и потоков **без GC** — ценно для real-time аудио (нет неожиданных
> пауз сборщика). Два пути: **standalone** (cpal + egui) или **плагин** (nih-plug, аналог JUCE).
> DSP-ядро выносим в отдельный крейт и переиспользуем в обоих.

> 🧭 Общие требования и роутинг — в [обзоре](README.md). Здесь — специфика Rust.

---

## 🧰 Выбор крейтов

```
   АУДИО-I/O:
   • cpal  ⭐ — кроссплатформенный захват/вывод (callback-модель). основа standalone-версии.

   GUI / КАРКАС:
   • nih-plug ⭐ — фреймворк аудиоплагинов (VST3/CLAP): параметры, real-time-дисциплина, GUI
     (egui/vizia) — «Rust-ответ JUCE». грузишь в OBS/DAW, хост роутит звук.
   • либо standalone GUI: egui (через eframe) — простые ползунки/метры/пресеты.

   REAL-TIME ОБМЕН (между потоками, без локов):
   • rtrb / ringbuf ⭐ — lock-free SPSC кольцевой буфер (захват⟷обработка⟷вывод). real-time-safe.
   • triple_buffer / arc-swap / atomic — передача ПАРАМЕТРОВ из UI в DSP без локов.

   DSP-ЯДРО (pitch + formant — «реализм»):
   • rustfft / realfft ⭐ — FFT → сам строишь phase-vocoder + формантный варпинг (учебно, полный контроль).
   • fundsp / dasp — DSP-примитивы, фильтры, эффекты (реверб, эквалайзер, ring-mod).
   • ⚠️ готового топового формант-питча в Rust мало → либо свой phase-vocoder (rustfft),
     либо FFI к C++ Rubber Band / SoundTouch (bindgen) ради качества. (честный нюанс Rust-экосистемы.)

   REAL-TIME КОНТРОЛЬ:
   • assert_no_alloc — ловит АЛЛОКАЦИИ в аудио-callback на этапе отладки (Rust-специфичный помощник).

   ML-уровень B (нейроконверсия RVC): ort (ONNX Runtime) / candle / tch (libtorch).
```

💡 Для «JUCE-подобного» опыта бери **nih-plug** (плагин + параметры + GUI + real-time из коробки).
Для своего окна — **cpal + egui**. «Реализм» (формант-сохраняющий питч) в Rust — это либо свой
phase-vocoder на `rustfft`, либо FFI к зрелой C++ библиотеке: Rust честно слабее C++ в готовом DSP,
но FFI решает (см. [Interop/FFI](../Interop/01-basics/03-ffi-idea.md)).

---

## 🏗️ Структура (Cargo workspace — переиспускаем ядро)

```
   voice-changer/                  (workspace)
   ├── Cargo.toml                  — [workspace] members = dsp, app, plugin
   ├── dsp/                        — БИБЛИОТЕЧНЫЙ крейт: чистое DSP, без I/O и GUI (тестируемо!)
   │   └── src/
   │       ├── lib.rs              — pub use; трейт Processor
   │       ├── pitch_formant.rs    — phase-vocoder ИЛИ FFI-обёртка (pitch + formant)
   │       ├── effects/            — reverb.rs, eq.rs, ringmod.rs, gate.rs
   │       ├── chain.rs            — цепочка эффектов
   │       └── params.rs           — Params (атомики/arc-swap), пресеты
   ├── app/                        — STANDALONE bin: cpal + egui
   │   └── src/main.rs             — устройства, ring buffers, окно с ползунками
   └── plugin/                     — ПЛАГИН: nih-plug (VST3/CLAP), тот же dsp
       └── src/lib.rs
```

💡 ⭐ Идиоматично для Rust: **DSP — отдельный крейт `dsp`** (чистый, без зависимостей на аудио/GUI),
а `app` и `plugin` его переиспользуют. Это прямое применение [модулей/крейтов Rust](../Rust/01-basics/07b-multiple-files.md):
ядро тестируешь юнит-тестами в изоляции, фронтенды — тонкие. Трейт `Processor` (как интерфейс) даёт
полиморфную цепочку эффектов.

---

## 🔄 Поток данных и потоки

```
   [Аудио-поток (real-time, cpal callback)]            [UI-поток (egui)]
   ────────────────────────────────────────            ─────────────────
   move |input, output| {                              ползунок →
     1. input → producer.push() (rtrb ring)              params.pitch.store(x)  (atomic/arc-swap)
     2. набрался кадр → dsp.process(frame)                  ↑ без локов, без аллокаций
        (pitch+formant → effect chain)                   метры ← читают атомики уровня
     3. output ← обработанные сэмплы
     ⚠️ ВНУТРИ: НЕТ Box/Vec::new/clone-в-heap, Mutex,
        println!, ?-проброс с аллокацией, panic!
   }
```

💡 ⭐⭐ Rust-нюанс: ownership спасает от **гонок данных**, но НЕ от нарушений real-time — ты всё ещё
обязан не аллоцировать и не блокироваться в аудио-callback. Передавай аудио через `rtrb` (lock-free),
параметры — через атомики/`arc-swap`. Оберни callback в `assert_no_alloc` при отладке — он
поймает случайный `Vec`/`Box`/`format!` в горячем пути.

---

## 🎛️ Параметры (UI → DSP без локов)

```rust
   use std::sync::atomic::{AtomicU32, Ordering};

   pub struct Params {
       pub pitch_semitones: AtomicU32,   // f32 в битах (atomic) — хранят как u32
       pub formant_shift:   AtomicU32,
       pub reverb_mix:      AtomicU32,
       pub robot:           std::sync::atomic::AtomicBool,
   }
   // UI: params.pitch_semitones.store(x.to_bits(), Ordering::Relaxed);
   // DSP: let pitch = f32::from_bits(params.pitch_semitones.load(Ordering::Relaxed));
```

```rust
   // ядро каждый кадр (раздельно pitch и formant = «реализм»):
   let pitch_scale   = 2f32.powf(pitch / 12.0);
   let formant_scale = 2f32.powf(formant / 12.0);
   self.vocoder.set_pitch(pitch_scale);
   self.vocoder.set_formant(formant_scale);   // НЕЗАВИСИМО → реалистичная смена тембра/пола
```

💡 ⭐⭐ Как и в C++, ключ реализма — **раздельные pitch и formant**. В `nih-plug` параметры ещё проще:
фреймворк сам даёт thread-safe `FloatParam`/`BoolParam` с автоматическим UI и сглаживанием — не надо
руками возиться с атомиками.

---

## 🔌 Вывод в виртуальный микрофон

```
   STANDALONE (cpal): открыть OUTPUT-стрим на устройство «VB-CABLE Input», писать туда out-буфер;
                      в Discord выбрать VB-CABLE как «микрофон». быстрый MVP.
   ПЛАГИН (nih-plug): собрать VST3/CLAP, загрузить в OBS/Voicemeeter/DAW — хост роутит звук сам,
                      ядро dsp переиспользуется без изменений.
   (свой виртуальный аудиодрайвер — отдельный сложный проект; на старте используй VB-CABLE.)
```

---

## ⚡ Производительность (Rust специфика)

```
   • НЕ аллоцировать в аудио-callback: буферы/FFT-планы/состояние — создать заранее, переиспользовать.
   • assert_no_alloc вокруг callback (debug) — мгновенно ловит случайные аллокации.
   • сборка --release, target-cpu=native; rustfft использует SIMD внутри.
   • избегай panic! в аудио-потоке (используй ветвление, а не unwrap на горячем пути).
   • денормали — обнуляй тихие хвосты (add-denormal / flush) чтобы не тормозить CPU.
   • размер блока cpal: меньше → ниже задержка, выше риск underrun; настраивай (256/512 @48кГц).
```

💡 Rust даёт «бесстрашную многопоточность» (компилятор не пустит гонку), но real-time-дисциплина —
на тебе. Это применение [владения/Send-Sync](../Rust/02-memory/10-borrow-checker.md) и
[профилирования](../ComputerScience/04-performance/25-profiling.md) к жёсткому реальному времени.

---

## 🗺️ План реализации (Rust)

```
   1. cpal passthrough: input → rtrb → output, без щелчков. (+ assert_no_alloc.)
   2. крейт dsp: трейт Processor + простой gain. Юнит-тест на буфере.
   3. phase-vocoder (rustfft) ИЛИ FFI к Rubber Band: pitch + formant. ← ядро реализма.
   4. effects (fundsp/свои): reverb, eq, ring-mod («робот»), gate. Цепочка.
   5. egui-окно: ползунки → Params (atomics), метры, пресеты (serde/JSON).
   6. вывод в VB-CABLE → тест в Discord. Затем plugin-крейт на nih-plug (VST3/CLAP).
   7. (Продвинуто) уровень B: RVC-инференс через ort/candle — нейроконверсия в целевой голос.
```

## ⚠️ Ловушки (Rust)

- ❌ Думать, что Rust сам решает real-time (он решает ГОНКИ, но не аллокации/локи в callback).
- ❌ `Mutex`/`Vec::new`/`format!`/`unwrap`-panic в аудио-потоке → щелчки/паника. (Лови `assert_no_alloc`.)
- ❌ Ждать готовый топовый формант-питч в крейтах — его мало; делай phase-vocoder или FFI.
- ❌ Только pitch без формант → «бурундук», не реализм.
- ❌ Передавать аудио через канал с аллокацией вместо `rtrb` (lock-free ring).
- ❌ Свой аудиодрайвер на старте — бери VB-CABLE.

➡️ Сравни с [🟦 C/C++ архитектурой](ARCHITECTURE-CPP.md) · вернуться к [обзору](README.md)
