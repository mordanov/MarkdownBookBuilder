"""EPUB renderer using Pandoc."""

from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.rendering.pandoc_base import PandocBaseRenderer


class EPUBRenderer(PandocBaseRenderer):
    """Pandoc-based EPUB3 renderer."""

    output_format = "epub3"

    def _get_default_extension(self) -> str:
        return ".epub"

    def _get_format_options(self, config: BookConfig) -> list[str]:
        """EPUB-specific options: include TOC, set chapter level."""
        return [
            "--toc",
            "--toc-depth=2",
        ]
