"""External plugin loader using Python entry points and config-based discovery."""

import importlib
import inspect
from collections.abc import Callable
from importlib.metadata import entry_points
from types import ModuleType

from markdown_book_builder.config.models import PluginsConfig
from markdown_book_builder.core.logging import get_logger
from markdown_book_builder.plugins.registry import (
    _registry,
    register_diagram_renderer,
    register_image_provider,
    register_renderer,
    register_validator,
    unregister_diagram_renderer,
    unregister_image_provider,
    unregister_renderer,
    unregister_validator,
)
from markdown_book_builder.rendering import Renderer

logger = get_logger(__name__)

_RENDERER_GROUP = "markdown_book_builder.renderers"
_DIAGRAM_GROUP = "markdown_book_builder.diagram_renderers"
_IMAGE_GROUP = "markdown_book_builder.image_providers"
_VALIDATOR_GROUP = "markdown_book_builder.validators"


def _load_renderer_ep(ep):  # type: ignore[no-untyped-def]
    """Load a renderer entry point. Returns True on success."""
    try:
        obj = ep.load()
        if not inspect.isclass(obj):
            logger.warning("Renderer entry point '%s' did not return a class, skipping", ep.name)
            return False
        if not issubclass(obj, Renderer):
            logger.warning(
                "Renderer entry point '%s' is not a subclass of Renderer, skipping", ep.name
            )
            return False
        register_renderer(ep.name, obj)
        logger.debug("Registered external renderer: %s -> %s", ep.name, obj.__name__)
        return True
    except Exception as exc:
        logger.warning("Failed to load renderer entry point '%s': %s", ep.name, exc)
        return False


def _load_diagram_renderer_ep(ep):  # type: ignore[no-untyped-def]
    """Load a diagram renderer entry point. Returns True on success."""
    from markdown_book_builder.plugins.diagram import DiagramRenderer

    try:
        obj = ep.load()
        if inspect.isclass(obj):
            if not issubclass(obj, DiagramRenderer):
                logger.warning(
                    "Diagram renderer entry point '%s' is not a subclass of "
                    "DiagramRenderer, skipping",
                    ep.name,
                )
                return False
            instance: DiagramRenderer = obj()
        elif isinstance(obj, DiagramRenderer):
            instance = obj
        else:
            logger.warning(
                "Diagram renderer entry point '%s' is not a DiagramRenderer, skipping",
                ep.name,
            )
            return False
        register_diagram_renderer(ep.name, instance)
        logger.debug("Registered external diagram renderer: %s", ep.name)
        return True
    except Exception as exc:
        logger.warning("Failed to load diagram renderer entry point '%s': %s", ep.name, exc)
        return False


def _load_image_provider_ep(ep):  # type: ignore[no-untyped-def]
    """Load an image provider entry point. Returns True on success."""
    from markdown_book_builder.plugins.image import ImageProvider

    try:
        obj = ep.load()
        if inspect.isclass(obj):
            if not issubclass(obj, ImageProvider):
                logger.warning(
                    "Image provider entry point '%s' is not a subclass of ImageProvider, skipping",
                    ep.name,
                )
                return False
            instance: ImageProvider = obj()
        elif isinstance(obj, ImageProvider):
            instance = obj
        else:
            logger.warning(
                "Image provider entry point '%s' is not an ImageProvider, skipping",
                ep.name,
            )
            return False
        register_image_provider(ep.name, instance)
        logger.debug("Registered external image provider: %s", ep.name)
        return True
    except Exception as exc:
        logger.warning("Failed to load image provider entry point '%s': %s", ep.name, exc)
        return False


def _load_validator_ep(ep):  # type: ignore[no-untyped-def]
    """Load a validator entry point. Returns True on success."""
    from markdown_book_builder.plugins.validator import Validator

    try:
        obj = ep.load()
        if inspect.isclass(obj):
            if not issubclass(obj, Validator):
                logger.warning(
                    "Validator entry point '%s' is not a subclass of Validator, skipping",
                    ep.name,
                )
                return False
            instance: Validator = obj()
        elif isinstance(obj, Validator):
            instance = obj
        else:
            logger.warning("Validator entry point '%s' is not a Validator, skipping", ep.name)
            return False
        register_validator(instance)
        logger.debug("Registered external validator: %s", ep.name)
        return True
    except Exception as exc:
        logger.warning("Failed to load validator entry point '%s': %s", ep.name, exc)
        return False


def _load_group(
    group: str,
    loader: Callable,  # type: ignore[type-arg]
) -> int:
    """Load all entry points from a group. Returns count loaded."""
    count = 0
    try:
        eps = entry_points(group=group)
    except Exception as exc:
        logger.warning("Failed to query entry points for group '%s': %s", group, exc)
        return 0
    for ep in eps:
        if loader(ep):
            count += 1
    return count


def _load_extra_plugin_module(module_path: str) -> bool:
    """Import a module from extra_plugins. Returns True on success.

    If the module exposes ``register_plugins(registry)``, calls it.
    Otherwise relies on module-level side effects (e.g. direct register_* calls).
    """
    try:
        module: ModuleType = importlib.import_module(module_path)
        if hasattr(module, "register_plugins") and callable(
            module.register_plugins  # type: ignore[attr-defined]
        ):
            module.register_plugins(_registry)  # type: ignore[attr-defined]
            logger.debug("Called register_plugins() in extra plugin module: %s", module_path)
        else:
            logger.debug("Imported extra plugin module: %s", module_path)
        return True
    except Exception as exc:
        logger.warning("Failed to import extra plugin module '%s': %s", module_path, exc)
        return False


def _apply_disabled(disabled: list[str]) -> None:
    """Unregister plugins listed as disabled from all registries."""
    for name in disabled:
        unregister_renderer(name)
        unregister_diagram_renderer(name)
        unregister_image_provider(name)
        unregister_validator(name)
        logger.debug("Disabled plugin: %s", name)


def load_external_plugins(config: PluginsConfig | None = None) -> int:
    """Load external plugins from Python entry points and optional config.

    Scans all four entry point groups, imports any ``extra_plugins`` modules,
    then applies the ``disabled`` list. Every individual failure emits a
    warning and is skipped rather than crashing.

    Args:
        config: Optional plugin configuration from ``book.toml``.

    Returns:
        Count of plugins successfully loaded/registered.
    """
    count = 0
    count += _load_group(_RENDERER_GROUP, _load_renderer_ep)
    count += _load_group(_DIAGRAM_GROUP, _load_diagram_renderer_ep)
    count += _load_group(_IMAGE_GROUP, _load_image_provider_ep)
    count += _load_group(_VALIDATOR_GROUP, _load_validator_ep)

    if config is not None:
        for module_path in config.extra_plugins:
            if _load_extra_plugin_module(module_path):
                count += 1
        if config.disabled:
            _apply_disabled(config.disabled)

    return count
