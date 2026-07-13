"""Tests for PluginRegistry unregister methods."""

import pytest

from markdown_book_builder.ast_.models import Book
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.errors import ValidationError
from markdown_book_builder.plugins.diagram import MermaidDiagramRenderer
from markdown_book_builder.plugins.image import ImageProvider
from markdown_book_builder.plugins.registry import PluginRegistry
from markdown_book_builder.plugins.validator import Validator
from markdown_book_builder.rendering import PandocRenderer


@pytest.fixture()
def registry() -> PluginRegistry:
    """Fresh registry instance for each test."""
    return PluginRegistry()


class TestUnregisterRenderer:
    def test_unregister_renderer(self, registry: PluginRegistry) -> None:
        registry.register_renderer("pdf-test", PandocRenderer)
        assert "pdf-test" in registry.list_renderer_names()
        registry.unregister_renderer("pdf-test")
        assert "pdf-test" not in registry.list_renderer_names()

    def test_unregister_nonexistent_renderer_does_not_raise(self, registry: PluginRegistry) -> None:
        registry.unregister_renderer("does-not-exist")

    def test_unregister_renderer_only_removes_named(self, registry: PluginRegistry) -> None:
        registry.register_renderer("keep", PandocRenderer)
        registry.register_renderer("remove", PandocRenderer)
        registry.unregister_renderer("remove")
        assert "keep" in registry.list_renderer_names()
        assert "remove" not in registry.list_renderer_names()

    def test_get_renderer_returns_none_after_unregister(self, registry: PluginRegistry) -> None:
        registry.register_renderer("pdf-test", PandocRenderer)
        registry.unregister_renderer("pdf-test")
        assert registry.get_renderer("pdf-test") is None


class TestUnregisterDiagramRenderer:
    def test_unregister_diagram_renderer(self, registry: PluginRegistry) -> None:
        mermaid = MermaidDiagramRenderer()
        registry.register_diagram_renderer("mermaid", mermaid)
        assert "mermaid" in registry.list_diagram_renderer_names()
        registry.unregister_diagram_renderer("mermaid")
        assert "mermaid" not in registry.list_diagram_renderer_names()

    def test_unregister_nonexistent_diagram_renderer_does_not_raise(
        self, registry: PluginRegistry
    ) -> None:
        registry.unregister_diagram_renderer("nonexistent")

    def test_get_diagram_renderer_returns_none_after_unregister(
        self, registry: PluginRegistry
    ) -> None:
        mermaid = MermaidDiagramRenderer()
        registry.register_diagram_renderer("mermaid", mermaid)
        registry.unregister_diagram_renderer("mermaid")
        assert registry.get_diagram_renderer("mermaid") is None


class TestUnregisterImageProvider:
    def test_unregister_image_provider(self, registry: PluginRegistry) -> None:
        class FakeProvider(ImageProvider):
            name = "fake"

            def get_image(self, key: str) -> bytes | None:
                return None

            def put_image(self, key: str, data: bytes) -> None:
                pass

        registry.register_image_provider("fake", FakeProvider())
        assert "fake" in registry.list_image_provider_names()
        registry.unregister_image_provider("fake")
        assert "fake" not in registry.list_image_provider_names()

    def test_unregister_nonexistent_image_provider_does_not_raise(
        self, registry: PluginRegistry
    ) -> None:
        registry.unregister_image_provider("nonexistent")


class TestUnregisterValidator:
    def test_unregister_validator_by_name(self, registry: PluginRegistry) -> None:
        class FakeValidator(Validator):
            name = "fake-validator"

            def validate(self, book: Book, config: BookConfig) -> list[ValidationError]:
                return []

        instance = FakeValidator()
        registry.register_validator(instance)
        assert len(registry.get_validators()) == 1
        registry.unregister_validator("fake-validator")
        assert len(registry.get_validators()) == 0

    def test_unregister_validator_nonexistent_name_does_not_raise(
        self, registry: PluginRegistry
    ) -> None:
        registry.unregister_validator("not-registered")

    def test_unregister_validator_only_removes_named(self, registry: PluginRegistry) -> None:
        class ValidatorA(Validator):
            name = "alpha"

            def validate(self, book: Book, config: BookConfig) -> list[ValidationError]:
                return []

        class ValidatorB(Validator):
            name = "beta"

            def validate(self, book: Book, config: BookConfig) -> list[ValidationError]:
                return []

        a, b = ValidatorA(), ValidatorB()
        registry.register_validator(a)
        registry.register_validator(b)
        registry.unregister_validator("alpha")
        remaining = registry.get_validators()
        assert len(remaining) == 1
        assert remaining[0] is b


class TestModuleLevelUnregisterFunctions:
    """Smoke-test that module-level functions delegate to the global registry."""

    def test_module_level_unregister_renderer(self) -> None:
        from markdown_book_builder.plugins.registry import (
            list_renderer_names,
            register_renderer,
            unregister_renderer,
        )

        register_renderer("_test_temp_", PandocRenderer)
        assert "_test_temp_" in list_renderer_names()
        unregister_renderer("_test_temp_")
        assert "_test_temp_" not in list_renderer_names()
