"""Configuration loader with TOML and environment variable support."""

from pathlib import Path
from typing import Any

from markdown_book_builder.config.models import BookConfig


def load_from_toml(path: str | Path) -> dict[str, Any]:
    """Load configuration from TOML file.

    Args:
        path: Path to TOML config file

    Returns:
        Parsed TOML as dictionary

    Raises:
        FileNotFoundError: If config file not found
    """
    # TODO: T012 - Implement TOML loading
    raise NotImplementedError("TOML loading to be implemented in Phase 2")


def load_env_overrides() -> dict[str, Any]:
    """Load configuration from environment variables.

    Looks for variables prefixed with BOOK_ or OPENAI_.

    Returns:
        Dictionary of environment-based config values
    """
    # TODO: T012 - Implement env var override support
    raise NotImplementedError("Env var loading to be implemented in Phase 2")


def load_config(config_path: str | Path = "book.toml") -> BookConfig:
    """Load and merge configuration from TOML and environment.

    Environment variables override TOML values.

    Args:
        config_path: Path to TOML config file

    Returns:
        Loaded and validated BookConfig

    Raises:
        FileNotFoundError: If config file not found
        ValidationError: If config is invalid
    """
    # TODO: T012 - Implement merged loading
    raise NotImplementedError("Config loading to be implemented in Phase 2")
