"""AST transformation utilities."""

from collections.abc import Callable
from typing import Any

from markdown_book_builder.ast_.models import Book


def traverse_book(book: Book, visitor: Callable[[Any], None]) -> None:
    """Traverse all nodes in a book AST.

    Args:
        book: Book AST to traverse
        visitor: Callable applied to each node
    """
    # TODO: T035 - Implement tree traversal
    raise NotImplementedError("Tree traversal to be implemented in Phase 4")


def transform_book(book: Book, transformer: Callable[[Any], Any]) -> Book:
    """Apply a transformation function to all nodes in a book AST.

    Args:
        book: Book AST to transform
        transformer: Function that transforms a node

    Returns:
        Transformed Book
    """
    # TODO: T035, T036, T037 - Implement transformation
    raise NotImplementedError("Tree transformation to be implemented in Phase 4")


def book_to_dict(book: Book) -> dict[str, Any]:
    """Serialize book AST to dictionary.

    Args:
        book: Book AST

    Returns:
        Dictionary representation
    """
    # TODO: T036 - Implement serialization
    return book.model_dump()


def dict_to_book(data: dict[str, Any]) -> Book:
    """Deserialize book AST from dictionary.

    Args:
        data: Dictionary representation

    Returns:
        Book AST
    """
    # TODO: T037 - Implement deserialization
    return Book.model_validate(data)
