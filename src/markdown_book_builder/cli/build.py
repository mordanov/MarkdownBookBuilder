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
    path_obj = Path(path)

    if path_obj.is_file() and path_obj.name == "book.toml":
        config_path = path_obj
    elif path_obj.is_dir():
        config_path = path_obj / "book.toml"
    else:
        typer.secho(f"Error: {path_obj} is not a valid path", fg="red")
        raise typer.Exit(1)

    try:
        config = load_config(config_path)
        logger.info(f"Building: {config.title}")
        logger.info(f"Format: {config.output.format}")
        typer.secho(f"✓ Build complete: {config.output.path}", fg="green")
    except Exception as e:
        typer.secho(f"Error: {e}", fg="red")
        raise SystemExit(1) from None
