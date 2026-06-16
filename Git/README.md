# 🌳 Трек · Git и код-ревью

> **Git — это память проекта.** Каждый разработчик пользуется им каждый день, но немногие понимают
> его модель. Этот трек — про то, как Git хранит историю, как работать с ветками, сотрудничать
> через pull request'ы и проводить код-ревью. Контроль версий и ревью — базовый навык командной
> разработки и обязательный пункт любого собеседования.

> 🧭 Дополняет [🧭 Senior-мышление](../Senior/01-craft/06-code-review.md) (код-ревью как практика) и
> [🛡️ безопасность](../Security/03-defensive-code/19-secrets-supply-chain.md) (секреты в репозитории).

---

## 🗺️ Дорожная карта

```mermaid
graph TD
    subgraph L0 [🥚 Уровень 0 — Введение]
        A0[00 · Зачем контроль версий]
        A1[01 · Что такое Git: снимки]
        A2[02 · Установка и настройка]
    end
    subgraph L1 [🐣 Уровень 1 — Основы]
        B0[03 · Репозиторий, staging, commit]
        B1[04 · История: log и diff]
        B2[05 · Отмена изменений]
        B3[06 · .gitignore]
        B4[07 · Хорошие коммиты]
    end
    subgraph L2 [🐥 Уровень 2 — Ветки и слияние ⭐ ядро]
        C0[08 · Ветки ⭐⭐]
        C1[09 · Слияние merge ⭐⭐]
        C2[10 · Конфликты слияния]
        C3[11 · Rebase]
        C4[12 · Merge vs rebase]
    end
    subgraph L3 [🦅 Уровень 3 — Совместная работа и ревью]
        D0[13 · Удалённые репозитории]
        D1[14 · Fetch, pull, push, tracking]
        D2[15 · Pull request / merge request]
        D3[16 · Код-ревью: автор и ревьюер]
        D4[17 · Рабочие процессы (workflow)]
    end
    subgraph L4 [🚀 Уровень 4 — Профи и восстановление]
        E0[18 · Интерактивный rebase]
        E1[19 · stash, cherry-pick, reflog]
        E2[20 · Теги, релизы, semver]
        E3[21 · Хуки и связь с CI]
        E4[22 · Большие репозитории, bisect]
        E5[23 · Восстановление и аварии]
    end
    L0 --> L1 --> L2 --> L3 --> L4 --> Done([🌳 Владею Git и ревью])
```

---

## 🎯 Ядро трека — Ветки и слияние

> **Сила Git — в дешёвых ветках:** изолируешь работу, экспериментируешь, потом сливаешь. Кто
> понимает ветвление, слияние, конфликты и rebase — понимает Git. Всё остальное (PR, workflow,
> восстановление) строится поверх этой модели.

Поэтому центр трека (Уровень 2) — от создания ветки до осознанного выбора merge vs rebase.

---

## 📂 Содержание

### 🥚 Уровень 0 — Введение
- [00 · Зачем нужен контроль версий](00-intro/00-why-version-control.md)
- [01 · Что такое Git: снимки, а не дельты](00-intro/01-what-is-git.md)
- [02 · Установка и настройка](00-intro/02-setup.md)

### 🐣 Уровень 1 — Основы
- [03 · Репозиторий, staging, commit](01-basics/03-repo-staging-commit.md)
- [04 · История: log и diff](01-basics/04-history-log-diff.md)
- [05 · Отмена изменений](01-basics/05-undoing-changes.md)
- [06 · .gitignore и что не коммитить](01-basics/06-gitignore.md)
- [07 · Анатомия хорошего коммита](01-basics/07-good-commits.md)
- ✅ [Задачи уровня 1](01-basics/TASKS.md) · 🚀 [Проект](01-basics/PROJECT.md)

### 🐥 Уровень 2 — Ветки и слияние ⭐ ядро
- [08 · Ветки ⭐⭐](02-branching/08-branches.md)
- [09 · Слияние (merge) ⭐⭐](02-branching/09-merge.md)
- [10 · Конфликты слияния](02-branching/10-conflicts.md)
- [11 · Rebase](02-branching/11-rebase.md)
- [12 · Merge vs rebase](02-branching/12-merge-vs-rebase.md)
- ✅ [Задачи уровня 2](02-branching/TASKS.md) · 🚀 [Проект](02-branching/PROJECT.md)

### 🦅 Уровень 3 — Совместная работа и ревью
- [13 · Удалённые репозитории](03-collaboration/13-remotes.md)
- [14 · Fetch, pull, push, tracking](03-collaboration/14-fetch-pull-push.md)
- [15 · Pull request / merge request](03-collaboration/15-pull-requests.md)
- [16 · Код-ревью: автор и ревьюер](03-collaboration/16-code-review.md)
- [17 · Рабочие процессы (workflow)](03-collaboration/17-workflows.md)
- ✅ [Задачи уровня 3](03-collaboration/TASKS.md) · 🚀 [Проект](03-collaboration/PROJECT.md)

### 🚀 Уровень 4 — Профи и восстановление
- [18 · Интерактивный rebase](04-pro/18-interactive-rebase.md)
- [19 · stash, cherry-pick, reflog](04-pro/19-stash-cherry-reflog.md)
- [20 · Теги, релизы, semver](04-pro/20-tags-releases.md)
- [21 · Хуки и связь с CI](04-pro/21-hooks-ci.md)
- [22 · Большие репозитории и bisect](04-pro/22-large-repos-bisect.md)
- [23 · Восстановление и аварии](04-pro/23-recovery.md)
- ✅ [Задачи уровня 4](04-pro/TASKS.md) · 🚀 [Проект](04-pro/PROJECT.md)

---

## 🧭 Как проходить

Git осваивается только **руками**. Заведи учебный репозиторий и повторяй каждую команду. Не бойся
ломать — почти всё в Git восстановимо (модуль 23). Сделай свой аккаунт на GitHub/GitLab и попробуй
весь цикл: ветка → коммиты → push → pull request → ревью → merge.

➡️ Начни с [00 · Зачем нужен контроль версий](00-intro/00-why-version-control.md)
