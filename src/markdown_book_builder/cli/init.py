"""Init command: Create new book project scaffold."""

from pathlib import Path

import typer

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


def init(path: str = typer.Argument(..., help="Path for new book project")) -> None:
    """Initialize a new book project scaffold.

    Creates directory structure, sample files, and configuration.
    """
    project_path = Path(path)

    if project_path.exists():
        typer.secho(f"Error: {path} already exists", fg="red")
        raise typer.Exit(1)

    try:
        project_path.mkdir(parents=True)
        (project_path / "content").mkdir()

        toml_content = """title = "My Book"
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

        readme = f"""# {path}

A book created with Markdown Book Builder.

## Usage

```bash
markdown-book-builder build .
```
"""
        (project_path / "README.md").write_text(readme)

        logger.info(f"Created new project: {path}")
        typer.secho(f"✓ Project initialized: {path}", fg="green")
    except Exception as e:
        typer.secho(f"Error: {e}", fg="red")
        raise SystemExit(1) from None
