"""High-level document discovery service."""

from pathlib import Path

from markdown_book_builder.ast_.models import Book
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.discovery.builder import build_ast_from_files
from markdown_book_builder.discovery.ordering import load_order_config, sort_chapters
from markdown_book_builder.discovery.scanner import scan_directory


def discover_book(source_dir: Path | str, config: BookConfig) -> Book:
    """Complete document discovery pipeline.

    Scans source directory for Markdown files, applies ordering,
    and builds the AST.

    Args:
        source_dir: Root directory to scan
        config: Book configuration

    Returns:
        Book AST

    Raises:
        ConfigurationError: If discovery fails
        FileNotFoundError: If source directory doesn't exist
    """
    source_path = Path(source_dir).resolve()

    try:
        files = scan_directory(source_path, recursive=True)

        if not files:
            raise ConfigurationError(f"No Markdown files found in {source_path}")

        order_file = source_path / "order.yaml"
        order = []
        if order_file.exists():
            order = load_order_config(order_file)

        files = sort_chapters(files, order)

        book = build_ast_from_files(files, config)
        return book

    except (FileNotFoundError, ValueError) as e:
        raise ConfigurationError(f"Document discovery failed: {e}") from e
