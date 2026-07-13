"""Pydantic configuration schema for TOML-based config."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class OpenAIConfig(BaseModel):
    """OpenAI API configuration."""

    api_key: str = Field(default="", description="OpenAI API key")
    model: str = Field(default="gpt-4o", description="OpenAI model to use")


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

    model_config = ConfigDict(extra="ignore")
