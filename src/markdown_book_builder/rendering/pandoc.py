from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.rendering.pandoc_base import PandocBaseRenderer


class PandocRenderer(PandocBaseRenderer):
    """Pandoc-based PDF renderer."""

    output_format = "pdf"

    def _get_default_extension(self) -> str:
        return ".pdf"

    def _get_format_options(self, config: BookConfig) -> list[str]:
        """Add PDF-specific pandoc options."""
        opts = ["--pdf-engine", config.output.pdf_engine]

        if config.output.pdf_engine == "xelatex":
            opts.extend(
                [
                    "-V",
                    "linestretch=1.5",
                    "--include-in-header",
                    self._get_xelatex_preamble(config),
                ]
            )

        return opts

    def _get_xelatex_preamble(self, config: BookConfig) -> str:
        """Create a temporary LaTeX preamble file for xelatex Unicode support."""
        import tempfile

        font = config.output.font
        preamble = rf"""
\usepackage{{polyglossia}}
\setmainlanguage{{english}}
\setotherlanguage{{russian}}
\setotherlanguage{{portuguese}}
\usepackage{{fontspec}}
\setmainfont{{{font}}}
\setsansfont{{{font}}}
\setmonofont{{Courier New}}
"""
        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write(preamble)
            return f.name
