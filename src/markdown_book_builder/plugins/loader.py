"""Plugin loader for built-in plugins."""

from markdown_book_builder.config.models import PluginsConfig
from markdown_book_builder.plugins.registry import (
    register_diagram_renderer,
    register_image_provider,
    register_renderer,
)
from markdown_book_builder.rendering import PandocRenderer


def load_builtin_plugins() -> None:
    """Load and register all built-in plugins."""
    # Register renderers
    from markdown_book_builder.rendering import DOCXRenderer, EPUBRenderer, HTMLRenderer

    register_renderer("pdf", PandocRenderer)
    register_renderer("html", HTMLRenderer)
    register_renderer("epub", EPUBRenderer)
    register_renderer("docx", DOCXRenderer)

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


def load_all_plugins(config: PluginsConfig | None = None) -> None:
    """Load built-in plugins and then external plugins.

    This is the primary entry point called at package import time.
    Pass a ``PluginsConfig`` from the loaded book config to also apply
    ``extra_plugins`` and ``disabled`` settings from ``book.toml``.

    Args:
        config: Optional plugin configuration. When ``None``, only
                entry-point discovery runs (no extra_plugins or disabled).
    """
    from markdown_book_builder.plugins.external import load_external_plugins

    load_builtin_plugins()
    load_external_plugins(config)
