"""Plugin system for extensible renderers, image providers, and validators."""

from markdown_book_builder.plugins.diagram import DiagramRenderer, MermaidDiagramRenderer
from markdown_book_builder.plugins.image import ImageProvider
from markdown_book_builder.plugins.loader import load_builtin_plugins
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
)
from markdown_book_builder.plugins.validator import Validator
from markdown_book_builder.rendering import Renderer

__all__ = [
    "DiagramRenderer",
    "ImageProvider",
    "MermaidDiagramRenderer",
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
    "load_builtin_plugins",
    "register_diagram_renderer",
    "register_image_provider",
    "register_renderer",
    "register_validator",
]
