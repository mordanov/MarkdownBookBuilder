"""Detect image placeholders in the AST."""

from pydantic import BaseModel

from markdown_book_builder.ast_.models import Book, Image, Section
from markdown_book_builder.ast_.transform import traverse_ast


class ImagePlaceholder(BaseModel):
    """Represents a detected image placeholder."""

    path: str
    alt_text: str
    caption: str | None = None
    node: Image | None = None


def detect_placeholders(book: Book) -> list[ImagePlaceholder]:
    """Detect all image placeholders in a book.

    Args:
        book: Book AST

    Returns:
        List of detected image placeholders
    """
    placeholders = []

    for node in traverse_ast(book):
        if isinstance(node, Image):
            placeholder = ImagePlaceholder(
                path=node.path,
                alt_text=node.alt_text,
                caption=node.caption,
                node=node,
            )
            placeholders.append(placeholder)

    return placeholders


def find_mermaid_diagrams(book: Book) -> list[str]:
    """Find all Mermaid diagram code blocks.

    Args:
        book: Book AST

    Returns:
        List of Mermaid diagram code strings
    """
    diagrams = []

    for node in traverse_ast(book):
        if isinstance(node, Section):
            if node.title and "diagram" in node.title.lower():
                diagrams.append(node.title)

    return diagrams
