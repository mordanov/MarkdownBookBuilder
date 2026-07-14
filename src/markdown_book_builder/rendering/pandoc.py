import tempfile

from markdown_book_builder.config.models import (
    BookConfig,
    FormattingConfig,
    get_effective_headings,
)
from markdown_book_builder.rendering.pandoc_base import PandocBaseRenderer

_LATEX_HEADING_COMMANDS = [
    "chapter",
    "section",
    "subsection",
    "subsubsection",
    "paragraph",
    "subparagraph",
]


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
        """Create a temporary LaTeX preamble file for xelatex."""
        font = config.output.font
        fmt = config.formatting

        base = rf"""
\usepackage{{polyglossia}}
\setmainlanguage{{english}}
\setotherlanguage{{russian}}
\setotherlanguage{{portuguese}}
\usepackage{{fontspec}}
\setmainfont{{{font}}}
\setsansfont{{{font}}}
\setmonofont{{Courier New}}
"""
        preamble = (
            base
            + self._page_layout_preamble(fmt)
            + self._heading_preamble(fmt)
            + self._hyperref_preamble(fmt)
        )

        with tempfile.NamedTemporaryFile(mode="w", suffix=".tex", delete=False) as f:
            f.write(preamble)
            return f.name

    def _page_layout_preamble(self, fmt: FormattingConfig) -> str:
        """Generate geometry package block for page layout."""
        p = fmt.page
        return (
            rf"\usepackage[{p.paper_size}paper,"
            rf"top={p.margin_top},"
            rf"bottom={p.margin_bottom},"
            rf"left={p.margin_left},"
            rf"right={p.margin_right}]{{geometry}}" + "\n"
        )

    def _heading_preamble(self, fmt: FormattingConfig) -> str:
        """Generate titlesec/xcolor heading format block."""
        headings = get_effective_headings(fmt.headings)
        lines = [r"\usepackage{titlesec}", r"\usepackage{xcolor}"]

        for (_key, style), cmd in zip(headings.items(), _LATEX_HEADING_COMMANDS, strict=True):
            size_cmd = _pt_to_latex_size(style.font_size)
            weight = r"\bfseries" if style.bold else r"\mdseries"
            shape = r"\itshape" if style.italic else r"\upshape"

            if style.background:
                # Heading with colored background bar.
                # \titleformat{cmd}[shape]{format}{label}{sep}{before-code}
                # #1 (heading text) must only appear in before-code (5th arg).
                lines.append(
                    rf"\titleformat{{\{cmd}}}[block]"
                    rf"{{{size_cmd}{weight}{shape}}}"
                    rf"{{}}"
                    rf"{{0em}}"
                    rf"{{\colorbox[HTML]{{{style.background}}}{{\parbox[t]{{\dimexpr\linewidth-2\fboxsep}}{{\color[HTML]{{{style.color}}}\strut #1\strut}}}}}}"
                )
            else:
                # Heading with text color only — label uses standard LaTeX counter command
                lines.append(
                    rf"\titleformat{{\{cmd}}}"
                    rf"{{{size_cmd}{weight}{shape}\color[HTML]{{{style.color}}}}}"
                    rf"{{\the{cmd}}}"
                    rf"{{1em}}{{}}"
                    rf"{{}}"
                )

        return "\n".join(lines) + "\n"

    def _hyperref_preamble(self, fmt: FormattingConfig) -> str:
        """Generate hyperref block for interactive TOC links."""
        if fmt.toc.interactive:
            return r"\usepackage[hidelinks]{hyperref}" + "\n"
        return ""


def _pt_to_latex_size(pt: int) -> str:
    """Map font size in pt to nearest LaTeX size command."""
    if pt >= 25:
        return r"\Huge "
    if pt >= 20:
        return r"\huge "
    if pt >= 17:
        return r"\LARGE "
    if pt >= 14:
        return r"\Large "
    if pt >= 12:
        return r"\large "
    if pt >= 10:
        return r"\normalsize "
    if pt >= 8:
        return r"\small "
    return r"\footnotesize "
