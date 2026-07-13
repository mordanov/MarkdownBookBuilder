"""Plugin system for extensible renderers, image providers, and validators."""

from markdown_book_builder.config.models import PluginsConfig
from markdown_book_builder.plugins.diagram import DiagramRenderer, MermaidDiagramRenderer
from markdown_book_builder.plugins.errors import PluginError, PluginLoadError, PluginNotFoundError
from markdown_book_builder.plugins.external import load_external_plugins
from markdown_book_builder.plugins.image import ImageProvider
from markdown_book_builder.plugins.loader import load_all_plugins, load_builtin_plugins
from markdown_book_builder.plugins.registry import (
    get_diagram_renderer,
    get_diagram_renderers,
    get_image_provider,
    get_image_providers,
    get_renderer,
    get_validators,
    list_diagram_renderer_names,
    list_image_provider_names,
    list_renderer_names,
    register_diagram_renderer,
    register_image_provider,
    register_renderer,
    register_validator,
    unregister_diagram_renderer,
    unregister_image_provider,
    unregister_renderer,
    unregister_validator,
)
from markdown_book_builder.plugins.validator import Validator
from markdown_book_builder.rendering import Renderer

__all__ = [
    "DiagramRenderer",
    "ImageProvider",
    "MermaidDiagramRenderer",
    "PluginError",
    "PluginLoadError",
    "PluginNotFoundError",
    "PluginsConfig",
    "Renderer",
    "Validator",
    "get_diagram_renderer",
    "get_diagram_renderers",
    "get_image_provider",
    "get_image_providers",
    "get_renderer",
    "get_validators",
    "list_diagram_renderer_names",
    "list_image_provider_names",
    "list_renderer_names",
    "load_all_plugins",
    "load_builtin_plugins",
    "load_external_plugins",
    "register_diagram_renderer",
    "register_image_provider",
    "register_renderer",
    "register_validator",
    "unregister_diagram_renderer",
    "unregister_image_provider",
    "unregister_renderer",
    "unregister_validator",
]
