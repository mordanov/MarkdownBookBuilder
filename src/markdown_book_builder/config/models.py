"""Pydantic configuration schema for TOML-based config."""

from pathlib import Path

from pydantic import BaseModel, Field


class OutputConfig(BaseModel):
    """Output format configuration."""

    format: str = Field(default="pdf", description="Output format (pdf, html, epub)")
    path: str | None = Field(default=None, description="Output file path")


class BookConfig(BaseModel):
    """Top-level book configuration schema."""

    title: str = Field(..., description="Book title")
    author: str | None = Field(default=None, description="Book author")
    version: str | None = Field(default="0.1.0", description="Book version")
    output: OutputConfig = Field(default_factory=OutputConfig, description="Output config")
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")

    class Config:
        """Pydantic config."""

        extra = "allow"  # Allow additional fields


def load_config(path: str | Path) -> BookConfig:
    """Load configuration from TOML file.

    Args:
        path: Path to TOML config file

    Returns:
        Parsed BookConfig

    Raises:
        FileNotFoundError: If config file not found
        ValidationError: If config is invalid
    """
    # TODO: T012 - Implement TOML loading with env var overrides
    raise NotImplementedError("Config loading to be implemented in Phase 2")
