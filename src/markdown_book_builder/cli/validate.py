"""Validate command: Check book structure and configuration."""

from pathlib import Path

import typer

from markdown_book_builder.config.loader import load_config
from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


def validate(
    path: str | Path = typer.Argument(".", help="Path to book project or book.toml"),
) -> None:
    """Validate book structure and configuration.

    Checks that all required files and configuration are valid.
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
        logger.info(f"Validating: {config.title}")
        typer.secho(f"✓ Validation passed: {config.title}", fg="green")
    except Exception as e:
        typer.secho(f"✗ Validation failed: {e}", fg="red")
        raise typer.Exit(1)
