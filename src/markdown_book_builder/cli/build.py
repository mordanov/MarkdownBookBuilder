"""Build command implementation."""
import typer

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


def build_book(path: str) -> None:
    """Build a book from Markdown files.
    
    Args:
        path: Path to Markdown directory or book.toml config
    """
    # TODO: US4 - Implement full build command
    logger.info(f"Building from {path}")
    raise NotImplementedError("Build command to be implemented in Phase 3")
