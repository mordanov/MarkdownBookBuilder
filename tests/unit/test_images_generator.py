"""Tests for image generation."""

import pytest

from markdown_book_builder.config.models import OpenAIConfig
from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.images.generator import (
    generate_placeholder_image,
)


def test_generate_image_no_api_key() -> None:
    """Test generation fails without API key."""
    config = OpenAIConfig(api_key="", model="gpt-4o")

    with pytest.raises(ConfigurationError) as exc_info:
        from markdown_book_builder.images.generator import generate_image

        generate_image("test prompt", config)

    assert "API key" in str(exc_info.value)


def test_generate_placeholder_image_no_api_key() -> None:
    """Test placeholder generation gracefully fails without API key."""
    config = OpenAIConfig(api_key="", model="gpt-4o")

    result = generate_placeholder_image("test", config)
    assert result is None


def test_generate_image_no_openai_library() -> None:
    """Test generation fails without openai library (gracefully)."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o")

    import sys

    openai_module = sys.modules.get("openai")

    try:
        if "openai" in sys.modules:
            del sys.modules["openai"]

        from markdown_book_builder.images.generator import generate_image

        with pytest.raises(ConfigurationError) as exc_info:
            generate_image("test", config)

        assert "openai" in str(exc_info.value).lower()

    finally:
        if openai_module:
            sys.modules["openai"] = openai_module


def test_generate_placeholder_invalid_config() -> None:
    """Test placeholder generation handles invalid config."""
    config = OpenAIConfig(api_key="", model="invalid")

    result = generate_placeholder_image("test prompt", config)
    assert result is None
