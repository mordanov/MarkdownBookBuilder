"""Image generation via OpenAI API."""

from markdown_book_builder.config.models import OpenAIConfig
from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


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
        logger.error("❌ API key not configured (empty or None)")
        raise ConfigurationError("OpenAI API key not configured")

    logger.info(f"🔑 Using API key: {config.api_key[:10]}...")
    logger.info(f"🤖 Using model: {config.image_model}")
    logger.info(f"📐 Image size: {size}")
    logger.info(f"📝 Prompt (first 100 chars): {prompt[:100]}...")

    try:
        import openai
    except ImportError:
        logger.error("❌ openai library not found")
        raise ConfigurationError("openai library not installed. Run: pip install openai") from None

    try:
        logger.info("🔄 Creating OpenAI client...")
        client = openai.OpenAI(api_key=config.api_key)

        logger.info("🔄 Calling images.generate()...")

        # Build request params based on model
        request_params = {
            "model": config.image_model,
            "prompt": prompt,
            "size": size,
            "n": 1,
        }

        # Model-specific parameters
        if config.image_model == "dall-e-3":
            request_params["quality"] = "standard"
        elif config.image_model in ("dall-e-2", "gpt-image-2"):
            # gpt-image-2 uses 'medium' as quality param
            request_params["quality"] = "medium"

        logger.info(f"📋 Request params: model={request_params['model']}, quality={request_params.get('quality', 'N/A')}, size={size}")
        response = client.images.generate(**request_params)

        logger.info(f"✓ API response received: {response}")

        if not response.data or not response.data[0].url:
            logger.error(f"❌ No image URL in response: {response}")
            raise ConfigurationError("No image URL in response")

        image_url = response.data[0].url
        logger.info(f"✓ Image URL: {image_url}")

        import urllib.request

        logger.info("🔄 Downloading image from URL...")
        with urllib.request.urlopen(image_url) as resp:
            image_data = resp.read()
            logger.info(f"✓ Image downloaded successfully ({len(image_data)} bytes)")
            return image_data  # type: ignore[no-any-return]

    except ConfigurationError:
        raise
    except Exception as e:
        logger.error(f"❌ Image generation failed: {type(e).__name__}: {e}")
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
    logger.info(f"🎨 Generating placeholder image for: {alt_text[:60]}...")
    try:
        result = generate_image(alt_text, config)
        logger.info("✓ Placeholder image generated successfully")
        return result
    except ConfigurationError as e:
        logger.error(f"❌ Failed to generate placeholder image: {e}")
        return None
