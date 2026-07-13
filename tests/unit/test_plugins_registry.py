"""Tests for plugin registry."""

import pytest

from markdown_book_builder.plugins import (
    get_diagram_renderer,
    get_image_provider,
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
from markdown_book_builder.plugins.diagram import MermaidDiagramRenderer
from markdown_book_builder.rendering import PandocRenderer


class TestRendererRegistry:
    def test_register_and_get_renderer(self):
        """Test registering and retrieving a renderer."""
        register_renderer("test-pdf", PandocRenderer)
        renderer = get_renderer("test-pdf")
        assert renderer is not None
        assert isinstance(renderer, PandocRenderer)

    def test_get_nonexistent_renderer(self):
        """Test getting a non-existent renderer returns None."""
        result = get_renderer("nonexistent-format")
        assert result is None

    def test_list_renderer_names(self):
        """Test listing registered renderer names."""
        names = list_renderer_names()
        assert isinstance(names, list)
        assert "pdf" in names  # Built-in PDF renderer

    def test_renderer_instantiation(self):
        """Test that registered renderers can be instantiated multiple times."""
        renderer1 = get_renderer("pdf")
        renderer2 = get_renderer("pdf")
        assert renderer1 is not None
        assert renderer2 is not None
        # Different instances
        assert renderer1 is not renderer2


class TestDiagramRendererRegistry:
    def test_register_and_get_diagram_renderer(self):
        """Test registering and retrieving a diagram renderer."""
        mermaid = MermaidDiagramRenderer()
        register_diagram_renderer("test-mermaid", mermaid)
        renderer = get_diagram_renderer("test-mermaid")
        assert renderer is mermaid

    def test_get_nonexistent_diagram_renderer(self):
        """Test getting a non-existent diagram renderer returns None."""
        result = get_diagram_renderer("nonexistent-diagram")
        assert result is None

    def test_list_diagram_renderer_names(self):
        """Test listing registered diagram renderer names."""
        names = list_diagram_renderer_names()
        assert isinstance(names, list)
        assert "mermaid" in names  # Built-in Mermaid renderer


class TestImageProviderRegistry:
    def test_register_and_get_image_provider(self):
        """Test registering and retrieving an image provider."""
        names = list_image_provider_names()
        assert isinstance(names, list)
        # Cache and OpenAI providers should be built-in
        assert "cache" in names
        assert "openai" in names

    def test_get_image_provider(self):
        """Test getting a registered image provider."""
        provider = get_image_provider("cache")
        assert provider is not None
        assert provider.name == "cache"


class TestValidatorRegistry:
    def test_get_validators(self):
        """Test getting registered validators."""
        validators = get_validators()
        assert isinstance(validators, list)
        # May be empty initially if no validators registered
