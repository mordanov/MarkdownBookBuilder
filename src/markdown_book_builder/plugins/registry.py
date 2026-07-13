"""Plugin registry for managing renderers, diagram renderers, and validators."""

from typing import TYPE_CHECKING, Any

from markdown_book_builder.rendering import Renderer

if TYPE_CHECKING:
    from markdown_book_builder.plugins.diagram import DiagramRenderer
    from markdown_book_builder.plugins.image import ImageProvider
    from markdown_book_builder.plugins.validator import Validator


class PluginRegistry:
    """Central registry for all plugin types."""

    def __init__(self) -> None:
        self._renderers: dict[str, type[Renderer]] = {}
        self._diagram_renderers: dict[str, Any] = {}
        self._image_providers: dict[str, Any] = {}
        self._validators: list[Any] = []

    def register_renderer(self, name: str, renderer_cls: type[Renderer]) -> None:
        """Register a renderer plugin."""
        self._renderers[name] = renderer_cls

    def get_renderer(self, name: str) -> Renderer | None:
        """Get a renderer instance by name."""
        if name not in self._renderers:
            return None
        renderer_cls = self._renderers[name]
        return renderer_cls()

    def list_renderer_names(self) -> list[str]:
        """List all registered renderer names."""
        return list(self._renderers.keys())

    def register_diagram_renderer(self, name: str, renderer: "DiagramRenderer") -> None:
        """Register a diagram renderer plugin."""
        self._diagram_renderers[name] = renderer

    def get_diagram_renderer(self, name: str) -> "DiagramRenderer | None":
        """Get a diagram renderer by name."""
        return self._diagram_renderers.get(name)

    def get_diagram_renderers(self) -> "dict[str, DiagramRenderer]":
        """Get all registered diagram renderers."""
        return dict(self._diagram_renderers)

    def list_diagram_renderer_names(self) -> list[str]:
        """List all registered diagram renderer names."""
        return list(self._diagram_renderers.keys())

    def register_image_provider(self, name: str, provider: "ImageProvider") -> None:
        """Register an image provider plugin."""
        self._image_providers[name] = provider

    def get_image_provider(self, name: str) -> "ImageProvider | None":
        """Get an image provider by name."""
        return self._image_providers.get(name)

    def get_image_providers(self) -> "dict[str, ImageProvider]":
        """Get all registered image providers."""
        return dict(self._image_providers)

    def list_image_provider_names(self) -> list[str]:
        """List all registered image provider names."""
        return list(self._image_providers.keys())

    def register_validator(self, validator: "Validator") -> None:
        """Register a validator plugin."""
        self._validators.append(validator)

    def get_validators(self) -> "list[Validator]":
        """Get all registered validators."""
        return list(self._validators)

    def unregister_renderer(self, name: str) -> None:
        """Unregister a renderer plugin by name. No-op if not registered."""
        self._renderers.pop(name, None)

    def unregister_diagram_renderer(self, name: str) -> None:
        """Unregister a diagram renderer plugin by name. No-op if not registered."""
        self._diagram_renderers.pop(name, None)

    def unregister_image_provider(self, name: str) -> None:
        """Unregister an image provider plugin by name. No-op if not registered."""
        self._image_providers.pop(name, None)

    def unregister_validator(self, name: str) -> None:
        """Remove validators whose 'name' attribute matches. No-op if none match."""
        self._validators = [
            v for v in self._validators if getattr(v, "name", None) != name
        ]


# Global singleton
_registry = PluginRegistry()


# Module-level convenience functions
def register_renderer(name: str, renderer_cls: type[Renderer]) -> None:
    """Register a renderer plugin."""
    _registry.register_renderer(name, renderer_cls)


def get_renderer(name: str) -> Renderer | None:
    """Get a renderer instance by name."""
    return _registry.get_renderer(name)


def list_renderer_names() -> list[str]:
    """List all registered renderer names."""
    return _registry.list_renderer_names()


def register_diagram_renderer(name: str, renderer: "DiagramRenderer") -> None:
    """Register a diagram renderer plugin."""
    _registry.register_diagram_renderer(name, renderer)


def get_diagram_renderer(name: str) -> "DiagramRenderer | None":
    """Get a diagram renderer by name."""
    return _registry.get_diagram_renderer(name)


def get_diagram_renderers() -> "dict[str, DiagramRenderer]":
    """Get all registered diagram renderers."""
    return _registry.get_diagram_renderers()


def list_diagram_renderer_names() -> list[str]:
    """List all registered diagram renderer names."""
    return _registry.list_diagram_renderer_names()


def register_image_provider(name: str, provider: "ImageProvider") -> None:
    """Register an image provider plugin."""
    _registry.register_image_provider(name, provider)


def get_image_provider(name: str) -> "ImageProvider | None":
    """Get an image provider by name."""
    return _registry.get_image_provider(name)


def get_image_providers() -> "dict[str, ImageProvider]":
    """Get all registered image providers."""
    return _registry.get_image_providers()


def list_image_provider_names() -> list[str]:
    """List all registered image provider names."""
    return _registry.list_image_provider_names()


def register_validator(validator: "Validator") -> None:
    """Register a validator plugin."""
    _registry.register_validator(validator)


def get_validators() -> "list[Validator]":
    """Get all registered validators."""
    return _registry.get_validators()


def unregister_renderer(name: str) -> None:
    """Unregister a renderer plugin by name."""
    _registry.unregister_renderer(name)


def unregister_diagram_renderer(name: str) -> None:
    """Unregister a diagram renderer plugin by name."""
    _registry.unregister_diagram_renderer(name)


def unregister_image_provider(name: str) -> None:
    """Unregister an image provider plugin by name."""
    _registry.unregister_image_provider(name)


def unregister_validator(name: str) -> None:
    """Unregister validators by name attribute."""
    _registry.unregister_validator(name)
