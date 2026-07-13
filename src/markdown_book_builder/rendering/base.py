from abc import ABC, abstractmethod
from pathlib import Path

from markdown_book_builder.ast_.models import Book
from markdown_book_builder.config.models import BookConfig


class Renderer(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the renderer is available on the system."""
        pass

    @abstractmethod
    def render(self, book: Book, config: BookConfig) -> Path:
        """Render book AST to output format.

        Args:
            book: Book AST with processed images
            config: Book configuration

        Returns:
            Path to the output file
        """
        pass
