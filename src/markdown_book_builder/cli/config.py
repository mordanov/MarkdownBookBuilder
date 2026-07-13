"""Config command: Show or validate configuration."""

from pathlib import Path

import typer

from markdown_book_builder.config.loader import load_config
from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


def config(
    path: str = typer.Option("book.toml", "--path", "-p", help="Path to configuration file"),
) -> None:
    """Show or validate configuration.

    Displays current configuration and validates schema.
    """
    try:
        cfg = load_config(Path(path))
        typer.echo(f"Title: {cfg.title}")
        typer.echo(f"Author: {cfg.author}")
        typer.echo(f"Version: {cfg.version}")
        typer.echo(f"Source Dir: {cfg.source_dir}")
        typer.echo(f"Output Format: {cfg.output.format}")
        typer.echo(f"Output Path: {cfg.output.path}")
        typer.echo(f"OpenAI Model: {cfg.openai.model}")
        typer.secho("✓ Configuration valid", fg="green")
    except Exception as e:
        typer.secho(f"Error: {e}", fg="red")
        raise SystemExit(1) from None
