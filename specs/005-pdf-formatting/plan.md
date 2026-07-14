# Implementation Plan: PDF Document Formatting Control

**Branch**: `005-pdf-formatting` | **Date**: 2026-07-14 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/005-pdf-formatting/spec.md`

## Summary

Добавить поддержку кастомизации PDF-форматирования через TOML-конфиг: стили заголовков H1–H6 (размер, цвет текста, цвет фона), полноширинный текст A4 с настраиваемыми полями, интерактивное оглавление с PDF-гиперссылками. Реализация через расширение LaTeX preamble в существующем `PandocRenderer` + новые Pydantic-модели в `BookConfig`.

## Technical Context

**Language/Version**: Python 3.13
**Primary Dependencies**: Pandoc + xelatex (LaTeX-пакеты: `titlesec`, `xcolor`, `geometry`, `hyperref`); Pydantic v2; Typer
**Storage**: N/A (только файловая генерация)
**Testing**: pytest (unit + integration)
**Target Platform**: macOS, Linux, Windows (через TeX Live / MiKTeX)
**Project Type**: CLI-инструмент / библиотека
**Performance Goals**: Время сборки не увеличивается (preamble генерируется раз за запуск)
**Constraints**: Обратная совместимость — существующие `book.toml` без `[formatting]` работают без изменений
**Scale/Scope**: Один TOML-файл конфигурации; 6 уровней заголовков; 4 поля страницы

## Constitution Check

Constitution-файл содержит только шаблонные плейсхолдеры без реальных правил — gates не применяются. Ни одного нарушения.

## Project Structure

### Documentation (this feature)

```text
specs/005-pdf-formatting/
├── plan.md              # Этот файл
├── research.md          # Phase 0: решения по технологиям
├── data-model.md        # Phase 1: Pydantic-модели FormattingConfig
├── quickstart.md        # Phase 1: руководство по конфигурации
├── contracts/
│   └── book_toml_schema.md   # Phase 1: контракт book.toml
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
src/markdown_book_builder/
├── config/
│   └── models.py                  # + FormattingConfig, HeadingStyleConfig,
│                                  #   PageLayoutConfig, TocConfig → в BookConfig
├── rendering/
│   └── pandoc.py                  # + генерация LaTeX preamble из FormattingConfig
└── (остальные модули без изменений)

tests/
├── unit/
│   ├── test_config_formatting.py  # NEW: валидация FormattingConfig
│   └── test_rendering_pandoc.py   # EXTENDED: preamble с formatting
└── integration/
    └── test_cli_build.py          # EXTENDED: сборка с кастомными стилями
```

**Structure Decision**: Single project (Option 1). Изменения изолированы в двух файлах — `config/models.py` и `rendering/pandoc.py`. Новые тесты в существующих директориях `unit/` и `integration/`.

## Complexity Tracking

Нет нарушений constitution — таблица не требуется.

---

## Phase 1: Design Artifacts

Все артефакты Phase 1 созданы:

- [research.md](research.md) — технические решения (LaTeX-пакеты, дефолтная тема, цвета)
- [data-model.md](data-model.md) — Pydantic-модели `FormattingConfig`, `HeadingStyleConfig`, `PageLayoutConfig`, `TocConfig`
- [contracts/book_toml_schema.md](contracts/book_toml_schema.md) — контракт `book.toml` с примерами и форматом ошибок
- [quickstart.md](quickstart.md) — руководство пользователя

---

## Implementation Outline (для /speckit-tasks)

### 1. Config models (`config/models.py`)

- Добавить `HeadingStyleConfig` (font_size, bold, italic, color, background)
- Добавить `PageLayoutConfig` (paper_size, margin_*)
- Добавить `TocConfig` (enabled, depth, interactive)
- Добавить `FormattingConfig` объединяющий headings h1–h6, page, toc
- Добавить поле `formatting: FormattingConfig` в `BookConfig`
- Pydantic-валидаторы для HEX-цветов и единиц измерения

### 2. Default theme constants

- Определить `DEFAULT_HEADING_STYLES: dict[str, HeadingStyleConfig]` с дефолтами из research.md Decision 7
- Функция `get_effective_formatting(config: FormattingConfig) -> FormattingConfig` — мержит пользовательские настройки с дефолтами

### 3. LaTeX preamble generation (`rendering/pandoc.py`)

- Рефакторинг `_get_xelatex_preamble()`: принимает `FormattingConfig`
- Генерация `\usepackage[...]{geometry}` из `PageLayoutConfig`
- Генерация `\usepackage{titlesec}` + `\usepackage{xcolor}` + `\titleformat{...}` для каждого H1–H6
- Генерация `\usepackage[hidelinks]{hyperref}` если `toc.interactive=True`
- Нормализация HEX-цветов (убрать `#`, uppercase)

### 4. Unit tests (`tests/unit/test_config_formatting.py`)

- Валидация корректных/некорректных HEX-цветов
- Валидация границ font_size
- Валидация формата полей страницы
- Дефолтные значения при пустом `[formatting]`
- Предупреждение при color == background

### 5. Unit tests (`tests/unit/test_rendering_pandoc.py`)

- Preamble содержит `\usepackage{geometry}` с правильными параметрами
- Preamble содержит `\titleformat` для H1 с нужными цветами
- Preamble содержит `\usepackage[hidelinks]{hyperref}` при `interactive=True`
- Preamble не содержит `hyperref` при `interactive=False`

### 6. Integration test (`tests/integration/test_cli_build.py`)

- Сборка с пустым `[formatting]` проходит (дефолты)
- Сборка с кастомными заголовками проходит
- Сборка с невалидным HEX завершается с ненулевым кодом

### 7. Обновить `book.toml` (example/template)

- Добавить закомментированный пример `[formatting]` в шаблон

### 8. Документация

- Обновить `USER_GUIDE.md`: секция "PDF Formatting"
