from abc import ABC, abstractmethod
from pathlib import Path

from markdown_book_builder.config.models import BookConfig


class Renderer(ABC):
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the renderer is available on the system."""
        pass

    @abstractmethod
    def render(self, files: list[Path], config: BookConfig) -> Path:
        """Render markdown files to output format.

        Args:
            files: Ordered list of Markdown file paths to render
            config: Book configuration

        Returns:
            Path to the output file
        """
        pass
