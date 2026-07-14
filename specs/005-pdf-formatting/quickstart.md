# Quickstart: PDF Formatting Configuration

## Минимальный старт (встроенная тема)

Ничего делать не нужно — при сборке PDF автоматически применяется встроенная тема с иерархией заголовков и полноширинным текстом A4.

```bash
python -m markdown_book_builder build .
```

## Кастомизация заголовков

Добавьте в `book.toml`:

```toml
[formatting.headings.h1]
font_size = 24
bold = true
color = "#FFFFFF"
background = "#003366"

[formatting.headings.h2]
font_size = 18
bold = true
color = "#003366"
```

## Изменение полей страницы

```toml
[formatting.page]
margin_left = "3cm"
margin_right = "2cm"
margin_top = "2cm"
margin_bottom = "2cm"
```

## Отключение гиперссылок в оглавлении

```toml
[formatting.toc]
interactive = false
```

## Проверка конфигурации

```bash
python -m markdown_book_builder validate .
```

Ошибки стилей выводятся до начала сборки PDF.
