"""Pydantic configuration schema for TOML-based config."""

import re
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, field_validator


def _normalize_hex_color(value: str) -> str:
    """Normalize HEX color: strip #, uppercase, validate 3 or 6 hex digits."""
    stripped = value.lstrip("#")
    if not re.fullmatch(r"[0-9A-Fa-f]{3}|[0-9A-Fa-f]{6}", stripped):
        raise ValueError(f"'{value}' is not a valid HEX color (expected #RRGGBB or #RGB)")
    return stripped.upper()


def _validate_margin(value: str) -> str:
    """Validate margin string matches CSS-like length format."""
    if not re.fullmatch(r"\d+(\.\d+)?(cm|mm|in|pt)", value):
        raise ValueError(
            f"'{value}' is not a valid margin (expected format: 2.5cm, 1in, 20mm, 10pt)"
        )
    numeric = float(re.match(r"\d+(\.\d+)?", value).group())  # type: ignore[union-attr]
    if numeric <= 0:
        raise ValueError(f"Margin '{value}' must be greater than 0")
    return value


class HeadingStyleConfig(BaseModel):
    """Style configuration for a single heading level (H1-H6)."""

    font_size: int = Field(default=12, ge=6, le=144, description="Font size in pt")
    bold: bool = Field(default=True, description="Bold weight")
    italic: bool = Field(default=False, description="Italic style")
    color: str = Field(default="000000", description="Text color as HEX (with or without #)")
    background: str | None = Field(
        default=None, description="Background color HEX; None = no background"
    )

    @field_validator("color", mode="before")
    @classmethod
    def validate_color(cls, v: str) -> str:
        return _normalize_hex_color(v)

    @field_validator("background", mode="before")
    @classmethod
    def validate_background(cls, v: str | None) -> str | None:
        if v is None:
            return None
        return _normalize_hex_color(v)

    model_config = ConfigDict(extra="ignore")


class PageLayoutConfig(BaseModel):
    """Page geometry configuration."""

    paper_size: str = Field(default="a4", description="Paper size identifier (a4, letter, etc.)")
    margin_top: str = Field(default="2.5cm", description="Top margin (e.g. 2.5cm, 1in)")
    margin_bottom: str = Field(default="2.5cm", description="Bottom margin")
    margin_left: str = Field(default="2.5cm", description="Left margin")
    margin_right: str = Field(default="2.5cm", description="Right margin")

    @field_validator("margin_top", "margin_bottom", "margin_left", "margin_right", mode="before")
    @classmethod
    def validate_margin(cls, v: str) -> str:
        return _validate_margin(v)

    model_config = ConfigDict(extra="ignore")


class TocConfig(BaseModel):
    """Table of contents configuration."""

    enabled: bool = Field(default=True, description="Generate table of contents")
    depth: int = Field(default=3, ge=1, le=6, description="Heading depth to include in TOC")
    interactive: bool = Field(default=True, description="Add PDF hyperlinks in TOC (hyperref)")

    model_config = ConfigDict(extra="ignore")


_DEFAULT_HEADING_STYLES: dict[str, HeadingStyleConfig] = {
    "h1": HeadingStyleConfig(font_size=22, bold=True, color="#FFFFFF", background="#1A3A5C"),
    "h2": HeadingStyleConfig(font_size=16, bold=True, color="#1A3A5C", background=None),
    "h3": HeadingStyleConfig(font_size=13, bold=True, color="#2C5282", background=None),
    "h4": HeadingStyleConfig(font_size=11, bold=True, color="#333333", background=None),
    "h5": HeadingStyleConfig(font_size=10, bold=True, color="#555555", background=None),
    "h6": HeadingStyleConfig(font_size=10, bold=False, color="#777777", background=None),
}


def get_effective_headings(
    headings: dict[str, HeadingStyleConfig],
) -> dict[str, HeadingStyleConfig]:
    """Merge user-supplied heading styles over defaults."""
    return {key: headings.get(key, default) for key, default in _DEFAULT_HEADING_STYLES.items()}


class FormattingConfig(BaseModel):
    """Document formatting configuration (headings, page layout, TOC)."""

    headings: dict[str, HeadingStyleConfig] = Field(
        default_factory=dict, description="Heading styles keyed by h1-h6"
    )
    page: PageLayoutConfig = Field(default_factory=PageLayoutConfig, description="Page geometry")
    toc: TocConfig = Field(default_factory=TocConfig, description="Table of contents options")

    model_config = ConfigDict(extra="ignore")


class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""

    api_key: str = Field(default="", description="OpenAI API key")
    model: str = Field(default="gpt-4o", description="OpenAI model to use")
    image_model: str = Field(default="dall-e-3", description="OpenAI model for image generation")
    grayscale: bool = Field(
        default=False,
        description="Generate images in grayscale (black & white) for print or token economy",
    )


class ThemeConfig(BaseModel):
    """Theme configuration for output styling."""

    name: str = Field(
        default="default", description="Theme name (default, dark, minimal) or path to CSS file"
    )


class PluginsConfig(BaseModel):
    """Plugin configuration for external and third-party plugins."""

    extra_plugins: list[str] = Field(
        default_factory=list,
        description="Module paths to import explicitly (e.g. 'mypkg.plugin')",
    )
    disabled: list[str] = Field(
        default_factory=list,
        description="Names of built-in or externally loaded plugins to disable",
    )


class OutputConfig(BaseModel):
    """Output format and path configuration."""

    format: str = Field(default="pdf", description="Output format (pdf, html, epub, docx)")
    path: Path = Field(default=Path("output/book.pdf"), description="Output file path")
    pdf_engine: str = Field(
        default="xelatex", description="PDF engine for pandoc (xelatex, pdflatex, wkhtmltopdf)"
    )
    font: str = Field(
        default="Verdana",
        description="Font for PDF output (Verdana, DejaVu Sans, Liberation Sans, etc.)",
    )
    cache_dir: Path = Field(
        default=Path(".cache/images"),
        description="Directory for caching generated images (relative to project root)",
    )


class BookConfig(BaseModel):
    """Top-level book configuration schema."""

    title: str = Field(..., description="Book title")
    author: str = Field(..., description="Book author")
    version: str = Field(default="1.0.0", description="Book version")
    source_dir: Path = Field(default=Path("."), description="Source directory for Markdown files")
    output: OutputConfig = Field(default_factory=OutputConfig, description="Output configuration")
    theme: ThemeConfig = Field(default_factory=ThemeConfig, description="Theme configuration")
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig, description="OpenAI configuration")
    plugins: PluginsConfig = Field(
        default_factory=PluginsConfig, description="Plugin configuration"
    )
    image_placeholder_format: str = Field(
        default="markdown",
        description="Image placeholder format: 'markdown' for ![alt](path) or 'brackets' for [ИЛЛЮСТРАЦИЯ N: description]",
    )
    formatting: FormattingConfig = Field(
        default_factory=FormattingConfig, description="PDF formatting configuration"
    )

    model_config = ConfigDict(extra="ignore")
