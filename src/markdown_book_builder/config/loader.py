"""Configuration loader with TOML and environment variable support."""

import os
import tomllib
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.errors import ConfigurationError


def load_from_toml(path: str | Path) -> dict[str, Any]:
    """Load configuration from TOML file.

    Args:
        path: Path to TOML config file

    Returns:
        Parsed TOML as dictionary

    Raises:
        ConfigurationError: If file not found or invalid TOML
    """
    path = Path(path)
    if not path.exists():
        raise ConfigurationError(f"Configuration file not found: {path}")

    try:
        with open(path, "rb") as f:
            return tomllib.load(f)
    except tomllib.TOMLDecodeError as e:
        raise ConfigurationError(f"Invalid TOML in {path}: {e}") from e


def load_env_overrides() -> dict[str, Any]:
    """Load configuration from environment variables.

    Looks for variables prefixed with BOOK_ or OPENAI_.
    Uses `__` as a nested separator (e.g., BOOK_OUTPUT__FORMAT).

    Returns:
        Dictionary of environment-based config values
    """
    config: dict[str, Any] = {}

    for key, value in os.environ.items():
        if key.startswith("BOOK_"):
            nested_key = key[5:].lower()
            if "__" in nested_key:
                parts = nested_key.split("__")
                current = config
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                config[nested_key] = value
        elif key == "OPENAI_API_KEY":
            if "openai" not in config:
                config["openai"] = {}
            config["openai"]["api_key"] = value

    return config


def _deep_merge(base: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    """Deep merge overrides into base dict (overrides take precedence).

    Args:
        base: Base configuration dictionary
        overrides: Override values to merge in

    Returns:
        Merged dictionary
    """
    result = base.copy()
    for key, value in overrides.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config(config_path: str | Path = "book.toml") -> BookConfig:
    """Load and merge configuration from TOML and environment.

    Environment variables override TOML values.

    Args:
        config_path: Path to TOML config file

    Returns:
        Loaded and validated BookConfig

    Raises:
        ConfigurationError: If config file not found or validation fails
    """
    config_dict: dict[str, Any] = {}

    path = Path(config_path)
    if path.exists():
        config_dict = load_from_toml(path)

    env_overrides = load_env_overrides()
    merged = _deep_merge(config_dict, env_overrides)

    try:
        return BookConfig(**merged)
    except ValidationError as e:
        raise ConfigurationError(f"Invalid configuration: {e}") from e
