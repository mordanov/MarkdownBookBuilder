"""Validate command: Check book structure and configuration."""

from pathlib import Path

import typer

from markdown_book_builder.config.loader import load_config
from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.core.logging import get_logger
from markdown_book_builder.discovery.service import discover_book

logger = get_logger(__name__)


def validate(
    path: str = typer.Argument(".", help="Path to book project or book.toml"),
) -> None:
    """Validate book structure and configuration.

    Checks that configuration is valid and all required Markdown files
    can be discovered and parsed successfully.

    Example:
        markdown-book-builder validate .
        markdown-book-builder validate /path/to/book.toml
    """
    path_obj = Path(path).resolve()

    if path_obj.is_file() and path_obj.name == "book.toml":
        config_path = path_obj
        project_dir = path_obj.parent
    elif path_obj.is_dir():
        config_path = path_obj / "book.toml"
        project_dir = path_obj
    else:
        typer.secho(f"Error: {path} is not a valid path", fg="red")
        raise SystemExit(1) from None

    try:
        typer.secho("✓ Checking configuration...", fg="cyan")
        config = load_config(config_path)

        source_dir = project_dir / config.source_dir

        typer.secho("✓ Validating document structure...", fg="cyan")
        book = discover_book(source_dir, config)

        typer.secho(
            f"✓ Validation passed: {book.title} ({len(book.chapters)} chapters)",
            fg="green",
        )
        logger.info("Book is ready to build")

    except ConfigurationError as e:
        typer.secho(f"✗ Configuration Error: {e}", fg="red")
        raise SystemExit(1) from None
    except Exception as e:
        typer.secho(f"✗ Validation failed: {e}", fg="red")
        logger.exception("Validation failed with exception")
        raise SystemExit(1) from None
