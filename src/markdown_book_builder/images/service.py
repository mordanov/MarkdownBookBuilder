"""High-level image processing service."""

import hashlib
from pathlib import Path

from markdown_book_builder.ast_.models import Book, Image
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.logging import get_logger
from markdown_book_builder.images.detector import detect_placeholders
from markdown_book_builder.images.generator import generate_placeholder_image
from markdown_book_builder.images.index import ImageIndex

logger = get_logger(__name__)


def process_images(book: Book, config: BookConfig) -> Book:
    """Process all images in a book.

    Detects image placeholders, checks cache, and generates missing images.
    Cache is stored in project directory.

    Args:
        book: Book AST
        config: Book configuration

    Returns:
        Updated book with generated images
    """
    placeholders = detect_placeholders(book)

    cache_dir = Path(config.output.cache_dir)
    index = ImageIndex(cache_dir)

    logger.info("=== IMAGE PROCESSING START ===")
    logger.info(f"Total placeholders found: {len(placeholders)}")
    logger.info(f"Cache directory: {cache_dir.absolute()}")
    logger.info(f"API Key configured: {bool(config.openai.api_key)}")

    generated = 0
    cached = 0
    skipped = 0

    for placeholder in placeholders:
        try:
            is_generated_placeholder = placeholder.path.startswith("image:")

            prompt_hash = _hash_prompt(placeholder.alt_text, config.openai.grayscale)
            cached_path = index.get(prompt_hash)

            if cached_path:
                logger.info(f"✓ Using cached image: {placeholder.alt_text[:50]}")
                if isinstance(placeholder.node, Image):
                    placeholder.node.path = str(cached_path)
                cached += 1
                continue

            if is_generated_placeholder:
                if not config.openai.api_key:
                    logger.warning(f"⊘ Skipping (no API key): {placeholder.alt_text[:50]}")
                    if isinstance(placeholder.node, Image):
                        placeholder.node.path = ""
                    skipped += 1
                    continue

                logger.info(f"🎨 Generating: {placeholder.alt_text[:50]}")
                image_data = generate_placeholder_image(
                    placeholder.alt_text,
                    config.openai,
                )

                if image_data:
                    image_path = _save_image(image_data, cache_dir, prompt_hash)
                    index.set(prompt_hash, image_path)
                    if isinstance(placeholder.node, Image):
                        placeholder.node.path = str(image_path)
                    generated += 1
                    logger.info(f"✓ Generated and cached: {image_path.name}")
                else:
                    if isinstance(placeholder.node, Image):
                        placeholder.node.path = ""
                    skipped += 1
            else:
                skipped += 1

        except Exception as e:
            logger.warning(f"Failed to process image: {e}")
            if isinstance(placeholder.node, Image):
                placeholder.node.path = ""
            skipped += 1

    logger.info("=== IMAGE PROCESSING COMPLETE ===")
    logger.info(f"Generated: {generated}, Cached: {cached}, Skipped: {skipped}")
    logger.info(f"Total: {generated + cached + skipped} / {len(placeholders)}")

    return book


def _hash_prompt(prompt: str, grayscale: bool = False) -> str:
    """Generate hash for image prompt, including color mode."""
    key = f"{'bw' if grayscale else 'color'}:{prompt}"
    return hashlib.sha256(key.encode()).hexdigest()


def _save_image(image_data: bytes, cache_dir: Path, prompt_hash: str) -> Path:
    """Save image to cache directory.

    Args:
        image_data: Image binary data
        cache_dir: Cache directory path
        prompt_hash: SHA256 hash of prompt

    Returns:
        Path to saved image
    """
    cache_dir.mkdir(parents=True, exist_ok=True)
    image_path = cache_dir / f"{prompt_hash}.png"
    image_path.write_bytes(image_data)
    logger.debug(f"💾 Saved image: {image_path} ({len(image_data)} bytes)")
    return image_path
