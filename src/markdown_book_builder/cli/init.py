"""Init command: Create new book project scaffold."""

from pathlib import Path

import typer

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)

SAMPLE_CHAPTER_1 = """---
title: Introduction
author: Your Name
date: 2026-07-13
---

# Welcome

This is your first chapter. Edit this file to get started.

## Getting Started

1. Edit content/chapter1.md with your content
2. Add more chapters in the content/ directory
3. Run `markdown-book-builder build .` to generate your book
"""

SAMPLE_CHAPTER_2 = """---
title: Chapter Two
---

# Your Second Chapter

Add your content here. Each Markdown file in the content/ directory
becomes a chapter in your book.

## Section

You can use standard Markdown syntax for headings, emphasis, code blocks, etc.
"""

ORDER_YAML = """# Chapter ordering (optional)
# Remove this file or leave empty to use alphabetical ordering
order:
  - chapter1.md
  - chapter2.md
"""


def init(path: str = typer.Argument(..., help="Path for new book project")) -> None:
    """Initialize a new book project scaffold.

    Creates directory structure, sample files, configuration, and README.

    Example:
        markdown-book-builder init my-book
        cd my-book
        markdown-book-builder build .
    """
    project_path = Path(path).resolve()

    if project_path.exists():
        typer.secho(f"Error: {path} already exists", fg="red")
        raise SystemExit(1) from None

    try:
        typer.secho("📁 Creating project structure...", fg="cyan")
        project_path.mkdir(parents=True)

        content_dir = project_path / "content"
        content_dir.mkdir()

        typer.secho("📝 Creating sample chapters...", fg="cyan")
        (content_dir / "chapter1.md").write_text(SAMPLE_CHAPTER_1)
        (content_dir / "chapter2.md").write_text(SAMPLE_CHAPTER_2)

        toml_content = """# Markdown Book Builder Configuration

title = "My Book"
author = "Author Name"
version = "1.0.0"
source_dir = "content"

[output]
format = "pdf"
path = "output/book.pdf"

[openai]
model = "gpt-4o"
"""
        (project_path / "book.toml").write_text(toml_content)

        (project_path / "order.yaml").write_text(ORDER_YAML)

        readme = """# My Book

A book created with Markdown Book Builder.

## Structure

- `content/` - Your Markdown chapter files
- `book.toml` - Project configuration
- `order.yaml` - Chapter ordering (optional)
- `output/` - Built book output

## Getting Started

1. Edit chapter files in `content/` directory
2. Add more chapters as needed
3. Update `order.yaml` to customize chapter order
4. Run `markdown-book-builder build .` to generate your book

## Usage

```bash
# Validate your book structure
markdown-book-builder validate .

# Build the book
markdown-book-builder build .

# View configuration
markdown-book-builder config .
```

## Next Steps

- [ ] Edit chapter1.md and chapter2.md with your content
- [ ] Add more chapters in the content/ directory
- [ ] Customize book.toml metadata
- [ ] Run build and check output/
"""
        (project_path / "README.md").write_text(readme)

        logger.info(f"Created new project: {project_path}")
        typer.secho(f"✓ Project initialized in {path}", fg="green")
        typer.secho(
            f"📚 Next steps:\n   cd {path}\n   markdown-book-builder build .",
            fg="blue",
        )

    except Exception as e:
        typer.secho(f"Error: {e}", fg="red")
        logger.exception("Init failed with exception")
        raise SystemExit(1) from None
