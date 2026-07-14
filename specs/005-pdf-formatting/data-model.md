# Data Model: PDF Document Formatting Control

## HeadingStyleConfig

Стиль одного уровня заголовка (H1–H6).

| Поле          | Тип            | Default     | Описание                                |
|---------------|----------------|-------------|-----------------------------------------|
| `font_size`   | `int`          | per-level   | Размер шрифта в pt                      |
| `bold`        | `bool`         | `True`      | Жирное начертание                       |
| `italic`      | `bool`         | `False`     | Курсив                                  |
| `color`       | `str`          | per-level   | Цвет текста HEX (с # или без)           |
| `background`  | `str \| None`  | `None`      | Цвет фона HEX; `None` = без фона        |

Validation rules:
- `font_size` ∈ [6, 144]
- `color` и `background` — валидные HEX-строки (3 или 6 цифр, с `#` или без)
- При `color == background` — предупреждение (невидимый текст), но не ошибка

## PageLayoutConfig

Параметры страницы.

| Поле           | Тип     | Default | Описание                         |
|----------------|---------|---------|----------------------------------|
| `paper_size`   | `str`   | `"a4"`  | Формат бумаги (a4, letter и др.) |
| `margin_top`   | `str`   | `"2.5cm"` | Верхнее поле                   |
| `margin_bottom`| `str`   | `"2.5cm"` | Нижнее поле                    |
| `margin_left`  | `str`   | `"2.5cm"` | Левое поле                     |
| `margin_right` | `str`   | `"2.5cm"` | Правое поле                    |

Validation rules:
- `paper_size` — строка, непустая
- Поля в форматах LaTeX/geometry: `2.5cm`, `1in`, `20mm` — regex: `^\d+(\.\d+)?(cm|mm|in|pt)$`
- Нулевые и отрицательные значения → ошибка валидации

## TocConfig

Конфигурация оглавления.

| Поле           | Тип   | Default | Описание                                |
|----------------|-------|---------|------------------------------------------|
| `enabled`      | `bool`| `True`  | Генерировать оглавление                  |
| `depth`        | `int` | `3`     | Глубина заголовков (1–6)                 |
| `interactive`  | `bool`| `True`  | Добавить PDF-гиперссылки (hyperref)      |

## FormattingConfig (новая секция в BookConfig)

Объединяющая конфигурация. Добавляется как поле `formatting` в `BookConfig`.

```toml
[formatting]

[formatting.page]
paper_size = "a4"
margin_top = "2.5cm"
margin_bottom = "2.5cm"
margin_left = "2.5cm"
margin_right = "2.5cm"

[formatting.toc]
enabled = true
depth = 3
interactive = true

[formatting.headings.h1]
font_size = 22
bold = true
color = "#FFFFFF"
background = "#1a3a5c"

[formatting.headings.h2]
font_size = 16
bold = true
color = "#1a3a5c"

[formatting.headings.h3]
font_size = 13
bold = true
color = "#2c5282"
```

## Дефолтные значения

При отсутствии секции `[formatting]` в `book.toml` применяется встроенная тема по умолчанию (описана в `research.md` → Decision 7). Это гарантирует, что существующие книги без конфигурации сразу получают улучшенное оформление.

## Связи с существующими моделями

- `FormattingConfig` добавляется как опциональное поле в существующий `BookConfig` (`config/models.py`)
- `PandocRenderer._get_xelatex_preamble()` получает `FormattingConfig` и генерирует соответствующий LaTeX preamble
- `ThemeConfig` не изменяется (CSS-тема для HTML остаётся отдельной концепцией)
