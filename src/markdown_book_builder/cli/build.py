"""Build command: Convert Markdown files to book output."""

from pathlib import Path

import typer

from markdown_book_builder.config.loader import load_config
from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.core.logging import get_logger
from markdown_book_builder.discovery.service import discover_book, discover_files
from markdown_book_builder.images.service import process_images
from markdown_book_builder.plugins import get_renderer

logger = get_logger(__name__)


def build(path: str = typer.Argument(".", help="Path to book project or book.toml")) -> None:
    """Build a book from Markdown files.

    Discovers Markdown files from source_dir, builds the AST, and renders to
    the specified output format (currently PDF via Pandoc/Typst).

    Example:
        markdown-book-builder build .
        markdown-book-builder build /path/to/book.toml
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
        typer.secho("📚 Loading configuration...", fg="cyan")
        config = load_config(config_path)

        source_dir = project_dir / config.source_dir

        typer.secho(f"🔍 Discovering documents in {source_dir}...", fg="cyan")
        book = discover_book(source_dir, config)
        files = discover_files(source_dir, config)

        typer.secho("🖼️  Processing images...", fg="cyan")
        book = process_images(book, config)

        typer.secho(f"📝 Rendering to {config.output.format.upper()}...", fg="cyan")
        renderer = get_renderer(config.output.format)
        if not renderer:
            typer.secho(f"Error: No renderer registered for '{config.output.format}'", fg="red")
            raise SystemExit(1) from None

        if not renderer.is_available():
            typer.secho(f"Error: {config.output.format} renderer not available", fg="red")
            raise SystemExit(1) from None

        output_path = renderer.render(book, config)

        typer.secho(
            f"✓ Build complete: {book.title} ({len(book.chapters)} chapters)",
            fg="green",
        )
        format_upper = config.output.format.upper()
        typer.secho(f"✓ {format_upper} written to {output_path}", fg="green")

    except ConfigurationError as e:
        typer.secho(f"Configuration Error: {e}", fg="red")
        raise SystemExit(1) from None
    except Exception as e:
        typer.secho(f"Build Error: {e}", fg="red")
        logger.exception("Build failed with exception")
        raise SystemExit(1) from None
