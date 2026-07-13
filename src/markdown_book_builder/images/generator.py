"""Image generation via OpenAI API."""

from markdown_book_builder.config.models import OpenAIConfig
from markdown_book_builder.core.errors import ConfigurationError


def generate_image(
    prompt: str,
    config: OpenAIConfig,
    size: str = "1024x1024",
) -> bytes:
    """Generate image via OpenAI API.

    Args:
        prompt: Image description/prompt
        config: OpenAI configuration
        size: Image size (1024x1024, 1024x1792, 1792x1024)

    Returns:
        Image data as bytes

    Raises:
        ConfigurationError: If API key not configured
    """
    if not config.api_key:
        raise ConfigurationError("OpenAI API key not configured")

    try:
        import openai  # type: ignore[import-not-found]
    except ImportError:
        raise ConfigurationError("openai library not installed. Run: pip install openai") from None

    try:
        client = openai.OpenAI(api_key=config.api_key)

        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size=size,
            quality="standard",
            n=1,
        )

        if not response.data or not response.data[0].url:
            raise ConfigurationError("No image URL in response")

        image_url = response.data[0].url

        import urllib.request

        with urllib.request.urlopen(image_url) as resp:
            return resp.read()  # type: ignore[no-any-return]

    except ConfigurationError:
        raise
    except Exception as e:
        raise ConfigurationError(f"Image generation failed: {e}") from e


def generate_placeholder_image(
    alt_text: str,
    config: OpenAIConfig,
) -> bytes | None:
    """Generate image from alt text.

    Args:
        alt_text: Alternative text describing the image
        config: OpenAI configuration

    Returns:
        Image data or None on error
    """
    try:
        return generate_image(alt_text, config)
    except ConfigurationError:
        return None
