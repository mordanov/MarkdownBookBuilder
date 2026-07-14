"""Tests for image generation."""

from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.config.models import OpenAIConfig
from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.images.generator import (
    generate_image,
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


def test_generate_image_success() -> None:
    """Test successful image generation via OpenAI API."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o", image_model="dall-e-3")
    test_image_data = b"\x89PNG\r\n\x1a\n"

    import sys

    mock_openai_module = MagicMock()
    mock_client = MagicMock()
    mock_openai_module.OpenAI.return_value = mock_client

    mock_response = MagicMock()
    mock_response.data = [MagicMock(url="https://example.com/image.png")]
    mock_client.images.generate.return_value = mock_response

    with (
        patch.dict(sys.modules, {"openai": mock_openai_module}),
        patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_resp = MagicMock()
        mock_resp.read.return_value = test_image_data
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        result = generate_image("test prompt", config)

        assert result == test_image_data
        mock_client.images.generate.assert_called_once_with(
            model="dall-e-3",
            prompt="test prompt",
            size="1024x1024",
            quality="standard",
            n=1,
            response_format="url",
        )
        mock_urlopen.assert_called_once_with("https://example.com/image.png")


def test_generate_image_uses_config_image_model() -> None:
    """Test that image model comes from config."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o", image_model="dall-e-3")
    test_image_data = b"\x89PNG\r\n\x1a\n"

    import sys

    mock_openai_module = MagicMock()
    mock_client = MagicMock()
    mock_openai_module.OpenAI.return_value = mock_client

    mock_response = MagicMock()
    mock_response.data = [MagicMock(url="https://example.com/image.png")]
    mock_client.images.generate.return_value = mock_response

    with (
        patch.dict(sys.modules, {"openai": mock_openai_module}),
        patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_resp = MagicMock()
        mock_resp.read.return_value = test_image_data
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        generate_image("test prompt", config)

        call_kwargs = mock_client.images.generate.call_args[1]
        assert call_kwargs["model"] == "dall-e-3"


def test_generate_image_no_url_in_response() -> None:
    """Test error handling when API returns no URL."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o")

    import sys

    mock_openai_module = MagicMock()
    mock_client = MagicMock()
    mock_openai_module.OpenAI.return_value = mock_client

    mock_response = MagicMock()
    mock_response.data = []
    mock_client.images.generate.return_value = mock_response

    with patch.dict(sys.modules, {"openai": mock_openai_module}):
        with pytest.raises(ConfigurationError) as exc_info:
            generate_image("test prompt", config)

        assert "No data in image response" in str(exc_info.value)


def test_generate_image_urlopen_fails() -> None:
    """Test error handling when image download fails."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o")

    import sys

    mock_openai_module = MagicMock()
    mock_client = MagicMock()
    mock_openai_module.OpenAI.return_value = mock_client

    mock_response = MagicMock()
    mock_response.data = [MagicMock(url="https://example.com/image.png")]
    mock_client.images.generate.return_value = mock_response

    with (
        patch.dict(sys.modules, {"openai": mock_openai_module}),
        patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_urlopen.side_effect = OSError("Network error")

        with pytest.raises(ConfigurationError) as exc_info:
            generate_image("test prompt", config)

        assert "generation failed" in str(exc_info.value).lower()


def test_generate_placeholder_image_success() -> None:
    """Test successful placeholder image generation."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o")
    test_image_data = b"\x89PNG\r\n\x1a\n"

    with patch("markdown_book_builder.images.generator.generate_image") as mock_gen:
        mock_gen.return_value = test_image_data

        result = generate_placeholder_image("a diagram", config)

        assert result == test_image_data
        mock_gen.assert_called_once_with("a diagram", config)


def test_generate_image_grayscale_prepends_prefix() -> None:
    """Grayscale mode prepends B&W instruction to prompt."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o", image_model="dall-e-3", grayscale=True)
    test_image_data = b"\x89PNG\r\n\x1a\n"

    import sys

    mock_openai_module = MagicMock()
    mock_client = MagicMock()
    mock_openai_module.OpenAI.return_value = mock_client

    mock_response = MagicMock()
    mock_response.data = [MagicMock(url="https://example.com/image.png")]
    mock_client.images.generate.return_value = mock_response

    with (
        patch.dict(sys.modules, {"openai": mock_openai_module}),
        patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_resp = MagicMock()
        mock_resp.read.return_value = test_image_data
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        generate_image("a cat", config)

        call_kwargs = mock_client.images.generate.call_args[1]
        assert call_kwargs["prompt"].startswith("Grayscale illustration")
        assert "a cat" in call_kwargs["prompt"]


def test_generate_image_grayscale_dalle2_uses_small_size() -> None:
    """Grayscale + dall-e-2 uses 512x512 for cost savings."""
    config = OpenAIConfig(api_key="sk-test", model="gpt-4o", image_model="dall-e-2", grayscale=True)
    test_image_data = b"\x89PNG\r\n\x1a\n"

    import sys

    mock_openai_module = MagicMock()
    mock_client = MagicMock()
    mock_openai_module.OpenAI.return_value = mock_client

    mock_response = MagicMock()
    mock_response.data = [MagicMock(url="https://example.com/image.png")]
    mock_client.images.generate.return_value = mock_response

    with (
        patch.dict(sys.modules, {"openai": mock_openai_module}),
        patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_resp = MagicMock()
        mock_resp.read.return_value = test_image_data
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        generate_image("a cat", config)

        call_kwargs = mock_client.images.generate.call_args[1]
        assert call_kwargs["size"] == "512x512"


def test_generate_image_grayscale_false_keeps_default_size() -> None:
    """Without grayscale, default size is preserved."""
    config = OpenAIConfig(
        api_key="sk-test", model="gpt-4o", image_model="dall-e-2", grayscale=False
    )
    test_image_data = b"\x89PNG\r\n\x1a\n"

    import sys

    mock_openai_module = MagicMock()
    mock_client = MagicMock()
    mock_openai_module.OpenAI.return_value = mock_client

    mock_response = MagicMock()
    mock_response.data = [MagicMock(url="https://example.com/image.png")]
    mock_client.images.generate.return_value = mock_response

    with (
        patch.dict(sys.modules, {"openai": mock_openai_module}),
        patch("urllib.request.urlopen") as mock_urlopen,
    ):
        mock_resp = MagicMock()
        mock_resp.read.return_value = test_image_data
        mock_resp.__enter__.return_value = mock_resp
        mock_urlopen.return_value = mock_resp

        generate_image("a cat", config)

        call_kwargs = mock_client.images.generate.call_args[1]
        assert call_kwargs["size"] == "1024x1024"
