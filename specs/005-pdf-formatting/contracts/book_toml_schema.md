# Contract: book.toml Formatting Schema

## Новая секция `[formatting]`

Добавляется в `book.toml` как опциональная секция. При отсутствии применяются дефолтные значения встроенной темы.

### Полный пример

```toml
[formatting]

[formatting.page]
paper_size = "a4"          # строка, непустая
margin_top = "2.5cm"       # формат: число + единица (cm, mm, in, pt)
margin_bottom = "2.5cm"
margin_left = "2.5cm"
margin_right = "2.5cm"

[formatting.toc]
enabled = true             # bool
depth = 3                  # int 1–6
interactive = true         # bool: добавлять PDF-гиперссылки

[formatting.headings.h1]
font_size = 22             # int 6–144
bold = true                # bool
italic = false             # bool
color = "#FFFFFF"          # HEX цвет текста (с # или без)
background = "#1a3a5c"     # HEX цвет фона (с # или без); отсутствие = нет фона

[formatting.headings.h2]
font_size = 16
bold = true
color = "#1a3a5c"
# background не указан → нет фона

[formatting.headings.h3]
font_size = 13
bold = true
color = "#2c5282"

[formatting.headings.h4]
font_size = 11
bold = true
color = "#333333"

[formatting.headings.h5]
font_size = 10
bold = true
color = "#555555"

[formatting.headings.h6]
font_size = 10
bold = false
color = "#777777"
```

### Ошибки конфигурации (FR-010)

Система завершает сборку с ненулевым кодом выхода и сообщением вида:

```
ConfigurationError: formatting.headings.h1.font_size: value 200 out of range [6, 144]
ConfigurationError: formatting.headings.h2.color: '#ZZZZZZ' is not a valid HEX color
ConfigurationError: formatting.page.margin_top: '0cm' must be > 0
```

### Совместимость

- Секция `[formatting]` полностью опциональна — существующие `book.toml` без неё работают без изменений.
- Можно переопределить только часть заголовков — остальные получат дефолтные стили.
