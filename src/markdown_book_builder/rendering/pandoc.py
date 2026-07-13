from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.rendering.pandoc_base import PandocBaseRenderer


class PandocRenderer(PandocBaseRenderer):
    """Pandoc-based PDF renderer."""

    output_format = "pdf"

    def _get_default_extension(self) -> str:
        return ".pdf"

    def _get_format_options(self, config: BookConfig) -> list[str]:
        """Add PDF-specific pandoc options."""
        return ["--pdf-engine", config.output.pdf_engine]
