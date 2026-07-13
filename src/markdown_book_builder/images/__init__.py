"""Image processing module for generating and caching images."""

from markdown_book_builder.images.cache import clear_cache, get_cached_image
from markdown_book_builder.images.detector import detect_placeholders
from markdown_book_builder.images.generator import generate_image
from markdown_book_builder.images.service import process_images

__all__ = [
    "clear_cache",
    "detect_placeholders",
    "generate_image",
    "get_cached_image",
    "process_images",
]
