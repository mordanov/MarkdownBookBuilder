"""High-level image processing service."""

from markdown_book_builder.ast_.models import Book, Image
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.logging import get_logger
from markdown_book_builder.images.cache import get_cache, get_cached_image
from markdown_book_builder.images.detector import detect_placeholders
from markdown_book_builder.images.generator import generate_placeholder_image

logger = get_logger(__name__)


def process_images(book: Book, config: BookConfig) -> Book:
    """Process all images in a book.

    Detects image placeholders, checks cache, and generates missing images.

    Args:
        book: Book AST
        config: Book configuration

    Returns:
        Updated book with generated images
    """
    placeholders = detect_placeholders(book)
    cache = get_cache()

    generated = 0
    cached = 0
    skipped = 0

    for placeholder in placeholders:
        try:
            is_generated_placeholder = placeholder.path.startswith("image:")

            cached_path = get_cached_image(placeholder.alt_text)

            if cached_path:
                logger.info(f"Using cached image for: {placeholder.alt_text}")
                if isinstance(placeholder.node, Image):
                    placeholder.node.path = str(cached_path)
                cached += 1
                continue

            if is_generated_placeholder:
                if not config.openai.api_key:
                    logger.warning(
                        f"Skipping image generation (no API key): {placeholder.alt_text}"
                    )
                    skipped += 1
                    continue

                logger.info(f"Generating image: {placeholder.alt_text}")
                image_data = generate_placeholder_image(
                    placeholder.alt_text,
                    config.openai,
                )

                if image_data:
                    cache.cache_image(placeholder.alt_text, image_data)
                    cached_path = get_cached_image(placeholder.alt_text)
                    if cached_path and isinstance(placeholder.node, Image):
                        placeholder.node.path = str(cached_path)
                    generated += 1
                    logger.info(f"Generated and cached: {placeholder.alt_text}")
                else:
                    skipped += 1
            else:
                skipped += 1

        except Exception as e:
            logger.warning(f"Failed to process image {placeholder.alt_text}: {e}")
            skipped += 1

    logger.info(
        f"Image processing complete: {generated} generated, {cached} cached, {skipped} skipped"
    )

    return book
