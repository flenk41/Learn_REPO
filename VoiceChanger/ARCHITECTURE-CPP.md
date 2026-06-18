# 🟦 Voice Changer — архитектура на C/C++

> Стек C/C++: зрелейшая экосистема real-time аудио. Рекомендуемый каркас — **JUCE** (даёт аудио-I/O,
> GUI и сборку как Standalone *или* VST-плагин одной кодовой базой). Ниже — структура, технологии,
> поток данных, потоки, и план.

> 🧭 Общие требования и роутинг — в [обзоре](README.md). Здесь — специфика C/C++.

---

## 🧰 Выбор технологий

```
   КАРКАС / GUI / АУДИО-УСТРОЙСТВА:
   • JUCE  ⭐ — фреймворк: аудио-устройства + GUI + Standalone/VST/AU из одного кода. лучший выбор.
     (альтернативы: только аудио — PortAudio / RtAudio / miniaudio; GUI — Dear ImGui / Qt.)

   DSP-ЯДРО (pitch + formant — «реализм»):
   • Rubber Band Library  ⭐ — качественный формант-сохраняющий pitch/time, есть real-time режим.
   • SoundTouch — проще/легче, тоже pitch+tempo (чуть ниже качество).
   • Signalsmith Stretch — современный, header-only, хороший phase-vocoder.
   • WORLD vocoder — высочайшее качество для ГОЛОСА (анализ/синтез), но тяжелее для realtime.
   • эффекты — собственные фильтры или juce::dsp (реверб, эквалайзер, овердрайв).

   СБОРКА: CMake. КОМПИЛЯТОР: MSVC / clang / gcc.
   (ML-уровень B: ONNX Runtime / libtorch для инференса RVC — продвинуто.)
```

💡 **JUCE** закрывает 80% инфраструктуры (устройства, callback, GUI, форматы), а «реализм» даёт
**Rubber Band** (формант-сохраняющий сдвиг). Это самый короткий путь к рабочему качественному
voice changer на C++.

> 🔬 КАК устроен сам алгоритм реализма (phase vocoder, разделение формант, PSOLA, эффекты) — в
> [DSP deep-dive](DSP-DEEPDIVE.md); понимая его, ты осознанно настраиваешь Rubber Band/WORLD, а не «крутишь вслепую».

---

## 🏗️ Слои и модули (предлагаемая структура)

```
   VoiceChanger/ (C++)
   ├── CMakeLists.txt
   ├── src/
   │   ├── main.cpp                    — точка входа (JUCE Application) / или PluginProcessor
   │   ├── audio/
   │   │   ├── AudioEngine.h/.cpp      — управление устройствами, callback, ring buffers
   │   │   └── RingBuffer.h            — lock-free SPSC буфер (захват⟷обработка⟷вывод)
   │   ├── dsp/
   │   │   ├── IProcessor.h            — интерфейс: process(float* in, float* out, int n)
   │   │   ├── PitchFormant.h/.cpp     — обёртка над Rubber Band (pitch + formant)
   │   │   ├── effects/                — Reverb, EQ, RingMod («робот»), NoiseGate
   │   │   └── EffectChain.h/.cpp      — цепочка эффектов по порядку
   │   ├── params/
   │   │   └── ParamStore.h            — атомарные/lock-free параметры (UI → DSP)
   │   ├── presets/
   │   │   └── PresetManager.h/.cpp    — загрузка/сохранение пресетов (JSON)
   │   └── ui/
   │       └── MainComponent.h/.cpp    — ползунки, пресеты, метры (juce::Component)
   └── third_party/  (JUCE, RubberBand, …)
```

💡 Разделяй **audio / dsp / params / ui** — это позволяет тестировать DSP отдельно от GUI и
переиспользовать ядро в Standalone и VST. `IProcessor` — общий интерфейс эффектов (см.
[ООП: полиморфизм](../OOP/02-pillars/11-polymorphism.md)) → цепочку эффектов легко собирать/менять.

---

## 🔄 Поток данных и потоки

```
   [Аудио-поток (real-time, приоритетный)]              [UI-поток (обычный)]
   ──────────────────────────────────────              ────────────────────
   audioDeviceIOCallback(in, out, n):                   ползунок изменён →
     1. in → ring buffer (capture)                        paramStore.pitch.store(x)  (atomic)
     2. набрался кадр (hop) → PitchFormant.process          ↑ без локов, без аллокаций
        → EffectChain.process                            метры ← читают атомики уровня
     3. out ← обработанные сэмплы
     4. (опц.) дублировать в виртуальный кабель
        ⚠️ ВНУТРИ: НЕТ new/delete, mutex, I/O, исключений!
```

💡 ⭐ Правило C++ real-time: аудио-callback — **священен**. Никаких `new`/`delete`, `std::mutex`,
файлов, логов, бросков исключений внутри. Память — выделить заранее (в `prepareToPlay`). Параметры
из UI — через `std::atomic` (lock-free). Нарушишь — получишь щелчки/выпадения звука.

---

## 🎛️ Параметры (UI → DSP без локов)

```cpp
   struct ParamStore {
       std::atomic<float> pitchSemitones { 0.0f };   // -12..+12 полутонов
       std::atomic<float> formantShift   { 0.0f };   // сдвиг формант (тембр/«пол»)
       std::atomic<float> reverbMix      { 0.0f };
       std::atomic<bool>  robot          { false };
       // UI пишет .store(), аудио-поток читает .load() — без mutex.
   };
```

```cpp
   // в DSP-ядре каждый кадр:
   float pitch   = params.pitchSemitones.load(std::memory_order_relaxed);
   float formant = params.formantShift.load(std::memory_order_relaxed);
   rubberBand.setPitchScale(std::pow(2.0, pitch / 12.0));
   rubberBand.setFormantScale(std::pow(2.0, formant / 12.0)); // раздельный формант = «реализм»
```

💡 ⭐⭐ Раздельные `setPitchScale` и `setFormantScale` (Rubber Band) — это и есть «реалистичность»:
меняешь высоту и тембр НЕЗАВИСИМО. «Женский» пресет = pitch ↑ + formant ↑ согласованно; «глубокий
мужской» = pitch ↓ + formant ↓.

---

## 🔌 Вывод в виртуальный микрофон

```
   MVP: выбрать в качестве OUTPUT-устройства виртуальный кабель (VB-CABLE), писать в него out-буфер;
        в Discord/игре выбрать этот кабель как «микрофон». (JUCE сам перечислит устройства.)
   PRO: оформить приложение как VST-плагин (JUCE PluginProcessor) и грузить в OBS/Voicemeeter —
        переиспользуешь то же DSP-ядро, хост сам роутит звук.
   (свой драйвер вирт. устройства на Windows — отдельный сложный проект, не для старта.)
```

---

## ⚡ Производительность (C++ специфика)

```
   • вся память — заранее (prepareToPlay): буферы, окна FFT, состояние Rubber Band. в callback — 0 аллокаций.
   • SIMD/векторизация и juce::dsp для горячих циклов; -O2/-O3, нативная архитектура.
   • размер блока: меньше → ниже задержка, но выше риск пропусков; настраивай (256/512 @48кГц).
   • профилируй (Tracy/VTune); следи, чтобы callback укладывался в дедлайн с запасом.
   • денормали — включи flush-to-zero (FTZ/DAZ), иначе тихий «хвост» реверба тормозит CPU.
```

💡 Связь с курсом: это прямое применение [быстрого кода и кэша](../ComputerScience/04-performance/22-cpu-bottlenecks.md)
и [ручного управления памятью](../C/02-memory/11-dynamic-memory.md) — здесь оно критично (реальное время).

---

## 🗺️ План реализации (C++)

```
   1. JUCE-проект (Standalone). Сквозной passthrough: вход → выход, без щелчков.
   2. ParamStore (atomics) + простейший эффект (gain) с ползунком в UI.
   3. Интегрировать Rubber Band: pitch + formant с двумя ползунками. ← ядро реализма.
   4. EffectChain: реверб/эквалайзер/ring-mod («робот»), шумодав.
   5. Пресеты (JSON) + метры уровня. Полировка UI.
   6. Роутинг в VB-CABLE → тест в Discord. (Опц.) VST-сборка.
   7. (Продвинуто) уровень B: RVC через ONNX Runtime — нейроконверсия в целевой голос.
```

## ⚠️ Ловушки (C++)

- ❌ Аллокации/локи/логи/исключения в аудио-callback → щелчки, выпадения.
- ❌ Только pitch-shift без формант → «бурундук», не реализм.
- ❌ Забыть flush-to-zero → денормали тормозят на тихих хвостах.
- ❌ Слишком большой буфер → заметная задержка (эхо в разговоре).
- ❌ Тащить свой драйвер вирт. устройства на старте (огромная сложность — бери VB-CABLE).
- ❌ Утечки/UB с указателями в DSP — используй RAII/умные указатели вне горячего пути.

➡️ Сравни с [🦀 Rust-архитектурой](ARCHITECTURE-RUST.md) · вернуться к [обзору](README.md)
