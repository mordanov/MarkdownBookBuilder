"""AST transformation utilities."""

from collections.abc import Generator
from typing import Any

from markdown_book_builder.ast_.models import (
    Book,
    Chapter,
    Paragraph,
    Section,
)


def traverse_ast(node: Any) -> Generator[Any]:
    """Traverse all nodes in an AST depth-first.

    Args:
        node: AST node to traverse (can be Book, Chapter, Section, etc.)

    Yields:
        Each node in the tree
    """
    yield node

    if isinstance(node, Book):
        for chapter in node.chapters:
            yield from traverse_ast(chapter)
    elif isinstance(node, Chapter):
        for child in node.children:
            yield from traverse_ast(child)
    elif isinstance(node, Section):
        for child in node.children:
            yield from traverse_ast(child)
    elif isinstance(node, Paragraph):
        for child in node.children:
            yield from traverse_ast(child)  # type: ignore[arg-type,union-attr]


def find_all_sections(book: Book) -> list[Section]:
    """Find all Section nodes in a book.

    Args:
        book: Book AST

    Returns:
        List of all Section nodes
    """
    sections = []
    for node in traverse_ast(book):
        if isinstance(node, Section):
            sections.append(node)
    return sections


def count_nodes(book: Book, node_type: type) -> int:
    """Count nodes of a specific type in a book.

    Args:
        book: Book AST
        node_type: Type of node to count (e.g., Text, Section)

    Returns:
        Count of matching nodes
    """
    count = 0
    for node in traverse_ast(book):
        if isinstance(node, node_type):
            count += 1
    return count


def get_headings(book: Book) -> list[str]:
    """Extract all section headings from a book.

    Args:
        book: Book AST

    Returns:
        List of section titles in order
    """
    headings = []
    for node in traverse_ast(book):
        if isinstance(node, Section):
            headings.append(node.title)
    return headings


def book_to_dict(book: Book) -> dict[str, Any]:
    """Serialize book AST to dictionary.

    Args:
        book: Book AST

    Returns:
        Dictionary representation
    """
    return book.model_dump()


def dict_to_book(data: dict[str, Any]) -> Book:
    """Deserialize book AST from dictionary.

    Args:
        data: Dictionary representation

    Returns:
        Book AST
    """
    return Book.model_validate(data)
