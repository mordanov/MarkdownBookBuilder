"""Plugin loader for built-in plugins."""

from markdown_book_builder.plugins.registry import (
    register_diagram_renderer,
    register_image_provider,
    register_renderer,
)
from markdown_book_builder.rendering import PandocRenderer


def load_builtin_plugins() -> None:
    """Load and register all built-in plugins."""
    # Register renderers
    register_renderer("pdf", PandocRenderer)

    # Register diagram renderers
    from markdown_book_builder.plugins.diagram import MermaidDiagramRenderer

    mermaid = MermaidDiagramRenderer()
    register_diagram_renderer("mermaid", mermaid)

    # Register image providers
    from markdown_book_builder.images.cache import get_cache
    from markdown_book_builder.plugins.image import ImageProvider

    class CacheImageProvider(ImageProvider):
        name = "cache"

        def get_image(self, key: str) -> bytes | None:
            cache = get_cache()
            path = cache.get_cached_image(key)
            if path:
                return path.read_bytes()
            return None

        def put_image(self, key: str, data: bytes) -> None:
            cache = get_cache()
            cache.cache_image(key, data)

    class OpenAIImageProvider(ImageProvider):
        name = "openai"

        def get_image(self, key: str) -> bytes | None:
            # OpenAI provider doesn't fetch existing images
            return None

        def put_image(self, key: str, data: bytes) -> None:
            # Store to cache
            cache = get_cache()
            cache.cache_image(key, data)

    register_image_provider("cache", CacheImageProvider())
    register_image_provider("openai", OpenAIImageProvider())
