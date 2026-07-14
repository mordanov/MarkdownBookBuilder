# Research: PDF Document Formatting Control

## Decision 1: PDF Renderer Target

**Decision**: Реализация через Pandoc + xelatex (текущий стек), не Typst.
**Rationale**: `src/markdown_book_builder/rendering/pandoc.py` уже использует xelatex через `--pdf-engine xelatex`. Typst упомянут в CLAUDE.md как будущий экспортёр, но ещё не реализован. Добавление всех трёх фич через xelatex пreamble — прямолинейное изменение существующего кода.
**Alternatives considered**: Typst — потребовал бы реализации нового рендерера с нуля, что выходит за рамки фичи.

---

## Decision 2: Стили заголовков — LaTeX пакет

**Decision**: Пакет `titlesec` + `xcolor` для стилизации заголовков по уровням.
**Rationale**: `titlesec` — стандартный LaTeX пакет для полного контроля над форматом заголовков (шрифт, размер, цвет текста). `xcolor` даёт `\colorbox{}{}` для цвета фона. Оба входят в стандартный дистрибутив TeX Live / MiKTeX.
**Alternatives considered**: `sectsty` — менее гибкий, не поддерживает цвет фона; `tcolorbox` — избыточен для простой подложки.

LaTeX команда для заголовка с фоном:
```latex
\titleformat{\section}[block]
  {\normalfont\Large\bfseries\color[HTML]{FFFFFF}\colorbox[HTML]{1a3a5c}
   {\parbox[t]{\dimexpr\linewidth-2\fboxsep}{\strut #1\strut}}}
  {}{0em}{}[\vspace{-0.5em}]
```

Без фона (только цвет текста):
```latex
\titleformat{\section}
  {\normalfont\Large\bfseries\color[HTML]{333333}}
  {\thesection}{1em}{}
```

---

## Decision 3: Разметка страницы A4 — пакет geometry

**Decision**: Пакет `geometry` с явными полями в preamble.
**Rationale**: `geometry` — стандартный способ задания страничной геометрии в LaTeX. Pandoc поддерживает его напрямую через `-V geometry:...`, но передача через preamble (`\usepackage[a4paper,...]{geometry}`) даёт полный контроль и лучше сочетается с существующей архитектурой preamble-файла.
**Alternatives considered**: `-V papersize:a4` в pandoc CLI — работает, но не даёт гибкого управления полями; текст в Markdown-режиме по умолчанию узкий из-за отсутствия geometry.

---

## Decision 4: Интерактивное оглавление — пакет hyperref

**Decision**: `\usepackage[hidelinks]{hyperref}` в preamble.
**Rationale**: Pandoc уже передаёт `--toc`, генерируя оглавление. Для PDF-гиперссылок нужен `hyperref`. Опция `hidelinks` убирает цветные рамки вокруг ссылок (визуально чистее). При необходимости пользователь может указать `colorlinks=true`.
**Alternatives considered**: `\usepackage[colorlinks=true]{hyperref}` — делает ссылки цветными, но визуально шумнее; для книг чаще предпочтителен `hidelinks`.

**Важно**: `hyperref` должен подключаться последним в preamble (или через `\AtBeginDocument`), чтобы избежать конфликтов с другими пакетами.

---

## Decision 5: Встроенные шрифты (Q2: только встроенные Typst)

**Decision**: Поскольку рендерер — xelatex (не Typst), "встроенные шрифты" интерпретируются как шрифты, уже используемые в проекте через fontspec: Verdana, DejaVu Sans, Courier New. Для заголовков поддерживаются варианты веса (Bold) через fontspec. Произвольные шрифты пользователь не задаёт — только размер, цвет и начертание (bold/italic).
**Rationale**: Соответствует духу ответа Q2 (без пользовательских шрифтов), адаптированного под реальный стек.

---

## Decision 6: Цветовые коды

**Decision**: Цвета задаются в формате HEX без `#` (например `1a3a5c`) или с `#` (например `#1a3a5c`) — оба варианта нормализуются при генерации LaTeX. LaTeX-команда `\color[HTML]{1A3A5C}` требует 6 hex-цифр без `#`.
**Rationale**: Pydantic-валидатор нормализует входные строки.

---

## Decision 7: Дефолтная тема заголовков

Встроенная тема по умолчанию (применяется без пользовательской конфигурации):

| Уровень | Размер | Bold | Цвет текста | Цвет фона   |
|---------|--------|------|-------------|-------------|
| H1      | 22pt   | да   | `#FFFFFF`   | `#1a3a5c`   |
| H2      | 16pt   | да   | `#1a3a5c`   | —           |
| H3      | 13pt   | да   | `#2c5282`   | —           |
| H4      | 11pt   | да   | `#333333`   | —           |
| H5      | 10pt   | да   | `#555555`   | —           |
| H6      | 10pt   | нет  | `#777777`   | —           |
