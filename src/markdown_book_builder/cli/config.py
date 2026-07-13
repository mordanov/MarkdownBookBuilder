"""Config command: Show or validate configuration."""

from pathlib import Path

import typer

from markdown_book_builder.config.loader import load_config
from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


def config(
    path: str = typer.Argument(".", help="Path to book project or book.toml"),
) -> None:
    """Show and validate book configuration.

    Displays all configuration settings and verifies the configuration
    is valid and ready to use.

    Example:
        markdown-book-builder config .
        markdown-book-builder config /path/to/book.toml
    """
    path_obj = Path(path).resolve()

    if path_obj.is_file() and path_obj.name == "book.toml":
        config_path = path_obj
    elif path_obj.is_dir():
        config_path = path_obj / "book.toml"
    else:
        typer.secho(f"Error: {path} is not a valid path", fg="red")
        raise SystemExit(1) from None

    try:
        cfg = load_config(config_path)

        typer.secho("\n📖 Book Configuration", fg="cyan", bold=True)
        typer.echo("─" * 40)
        typer.echo(f"Title:          {cfg.title}")
        typer.echo(f"Author:         {cfg.author}")
        typer.echo(f"Version:        {cfg.version}")
        typer.echo()

        typer.secho("📁 Source & Output", fg="cyan", bold=True)
        typer.echo("─" * 40)
        typer.echo(f"Source Dir:     {cfg.source_dir}")
        typer.echo(f"Output Format:  {cfg.output.format}")
        typer.echo(f"Output Path:    {cfg.output.path}")
        typer.echo()

        typer.secho("🤖 AI Configuration", fg="cyan", bold=True)
        typer.echo("─" * 40)
        typer.echo(f"Model:          {cfg.openai.model}")
        has_api_key = bool(cfg.openai.api_key)
        typer.echo(f"API Key:        {'✓ Configured' if has_api_key else '✗ Not set'}")
        typer.echo()

        typer.secho("✓ Configuration valid and ready to use", fg="green")
        logger.info(f"Configuration loaded from {config_path}")

    except ConfigurationError as e:
        typer.secho(f"✗ Configuration Error: {e}", fg="red")
        raise SystemExit(1) from None
    except Exception as e:
        typer.secho(f"✗ Error loading configuration: {e}", fg="red")
        logger.exception("Config load failed with exception")
        raise SystemExit(1) from None
