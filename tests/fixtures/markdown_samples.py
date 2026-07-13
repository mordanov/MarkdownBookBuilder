"""Sample Markdown strings for testing."""

MINIMAL_MARKDOWN = """# Heading

Simple paragraph.
"""

MARKDOWN_WITH_FRONT_MATTER = """---
title: Test Document
author: Test Author
tags:
  - example
  - test
---

# Introduction

This is the introduction.
"""

MARKDOWN_WITH_CODE_BLOCK = """# Code Example

Here's some Python code:

```python
def hello():
    print("world")
```

And that's it.
"""

MARKDOWN_WITH_IMAGE = """# Images

Here's an image:

![Alt text](image.png "Image caption")

Pretty cool!
"""

EMPTY_MARKDOWN = ""

UNICODE_MARKDOWN = """# Unicode Test

Here's some unicode content:

- 你好世界 (Hello World in Chinese)
- مرحبا بالعالم (Hello World in Arabic)
- Привет мир (Hello World in Russian)
- 🚀 Rocket emoji

This tests proper unicode handling.
"""

MULTI_HEADING_MARKDOWN = """# Level 1

Some content here.

## Level 2

More content.

### Level 3

Even more content.

#### Level 4

Going deeper.

##### Level 5

Very deep.

###### Level 6

Deepest level.
"""

MARKDOWN_WITH_MULTIPLE_PARAGRAPHS = """# Multiple Paragraphs

This is the first paragraph.
It has multiple lines.
But it's still one paragraph.

This is the second paragraph.
It's separate from the first.

This is the third paragraph.
"""

MARKDOWN_WITH_NESTED_LISTS = """# Nested Lists

- Item 1
  - Subitem 1.1
  - Subitem 1.2
    - Subsubitem 1.2.1
- Item 2
  - Subitem 2.1
- Item 3
"""

MARKDOWN_WITH_MIXED_CONTENT = """# Mixed Content

This is a paragraph with **bold** and *italic* text.

```python
# A code block
x = 42
```

Another paragraph with a [link](https://example.com).

![An image](img.png)

- A list
- With items
"""
