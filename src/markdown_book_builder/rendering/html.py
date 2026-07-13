"""HTML renderer using Pandoc."""

from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.rendering.pandoc_base import PandocBaseRenderer


class HTMLRenderer(PandocBaseRenderer):
    """Pandoc-based HTML5 renderer."""

    output_format = "html5"

    def _get_default_extension(self) -> str:
        return ".html"

    def _get_format_options(self, config: BookConfig) -> list[str]:
        """HTML-specific options: standalone with TOC in HTML."""
        return [
            "--standalone",
            "--self-contained",
        ]
