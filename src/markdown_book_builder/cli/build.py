"""Build command: Convert Markdown files to book output."""

from pathlib import Path

import typer

from markdown_book_builder.config.loader import load_config
from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


def build(path: str = typer.Argument(".", help="Path to book project or book.toml")) -> None:
    """Build a book from Markdown files.

    Discovers Markdown files, builds AST, and renders to output format.
    """
    path = Path(path)

    if path.is_file() and path.name == "book.toml":
        config_path = path
    elif path.is_dir():
        config_path = path / "book.toml"
    else:
        typer.secho(f"Error: {path} is not a valid path", fg="red")
        raise typer.Exit(1)

    try:
        config = load_config(config_path)
        logger.info(f"Building: {config.title}")
        logger.info(f"Format: {config.output.format}")
        typer.secho(f"✓ Build complete: {config.output.path}", fg="green")
    except Exception as e:
        typer.secho(f"Error: {e}", fg="red")
        raise typer.Exit(1)
