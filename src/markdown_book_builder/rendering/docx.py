"""DOCX renderer using Pandoc."""

from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.rendering.pandoc_base import PandocBaseRenderer


class DOCXRenderer(PandocBaseRenderer):
    """Pandoc-based DOCX (Microsoft Word) renderer."""

    output_format = "docx"

    def _get_default_extension(self) -> str:
        return ".docx"

    def _get_format_options(self, config: BookConfig) -> list[str]:
        """DOCX-specific options: TOC, reference doc for styling."""
        return [
            "--toc",
            "--toc-depth=2",
        ]
