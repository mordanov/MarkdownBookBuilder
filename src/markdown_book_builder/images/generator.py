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

        # Model-specific parameters
        quality_param = "standard"
        if config.image_model in ("dall-e-2", "gpt-image-2"):
            quality_param = "medium"

        # Build request params dict - only add supported parameters for each model
        request_kwargs = {
            "model": config.image_model,
            "prompt": prompt,
            "size": size,
            "quality": quality_param,
            "n": 1,
        }

        # response_format only supported by dall-e models, not gpt-image-2
        if config.image_model in ("dall-e-2", "dall-e-3"):
            request_kwargs["response_format"] = "url"

        logger.info(
            f"📋 Request params: model={config.image_model}, quality={quality_param}, "
            f"response_format={'url' if config.image_model in ('dall-e-2', 'dall-e-3') else 'default'}, size={size}"
        )
        response = client.images.generate(**request_kwargs)  # type: ignore[call-overload]

        logger.info("✓ API response received")
        logger.info(f"📊 Response type: {type(response)}")
        logger.info(f"📊 Response attributes: {dir(response)}")
        logger.info(
            f"📊 Response data: {response.data if hasattr(response, 'data') else 'NO DATA ATTR'}"
        )

        if not hasattr(response, "data") or not response.data:
            logger.error(f"❌ No data in response. Full response: {response}")
            raise ConfigurationError("No data in image response")

        image_data_obj = response.data[0]
        logger.info(
            f"📊 Image object: url={bool(image_data_obj.url)}, b64_json={bool(image_data_obj.b64_json)}"
        )

        # Handle both URL and base64 response formats
        if image_data_obj.url:
            logger.info("✓ Got URL response format")
            image_url = image_data_obj.url
            logger.info(f"✓ Image URL: {image_url}")

            import urllib.request

            logger.info("🔄 Downloading image from URL...")
            with urllib.request.urlopen(image_url) as resp:
                image_data = resp.read()
                logger.info(f"✓ Image downloaded successfully ({len(image_data)} bytes)")
                return image_data  # type: ignore[no-any-return]

        elif image_data_obj.b64_json:
            logger.info("✓ Got base64 response format")
            import base64

            image_data = base64.b64decode(image_data_obj.b64_json)
            logger.info(f"✓ Decoded image: {len(image_data)} bytes")
            return image_data

        else:
            logger.error(f"❌ No URL or base64 data in response: {image_data_obj}")
            raise ConfigurationError("No image data in response")

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
