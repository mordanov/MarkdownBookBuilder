"""Validator plugins."""

from abc import ABC, abstractmethod

from markdown_book_builder.ast_.models import Book
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.errors import ValidationError


class Validator(ABC):
    """Base class for content validators."""

    name: str

    @abstractmethod
    def validate(self, book: Book, config: BookConfig) -> list[ValidationError]:
        """Validate book content.

        Args:
            book: Book AST to validate
            config: Book configuration

        Returns:
            List of validation errors (empty if valid)
        """
        pass
