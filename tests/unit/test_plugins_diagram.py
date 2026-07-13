"""Tests for diagram renderer plugins."""

from unittest.mock import patch

import pytest

from markdown_book_builder.plugins.diagram import MermaidDiagramRenderer


@pytest.fixture
def mermaid_renderer():
    return MermaidDiagramRenderer()


class TestMermaidDiagramRenderer:
    def test_name(self, mermaid_renderer):
        """Test renderer name."""
        assert mermaid_renderer.name == "mermaid"

    def test_is_available_true(self, mermaid_renderer):
        """Test is_available when mmdc is on PATH."""
        with patch("shutil.which", return_value="/usr/bin/mmdc"):
            assert mermaid_renderer.is_available() is True

    def test_is_available_false(self, mermaid_renderer):
        """Test is_available when mmdc is not on PATH."""
        with patch("shutil.which", return_value=None):
            assert mermaid_renderer.is_available() is False

    def test_supports_graph(self, mermaid_renderer):
        """Test supports for graph type."""
        assert mermaid_renderer.supports("graph") is True

    def test_supports_flowchart(self, mermaid_renderer):
        """Test supports for flowchart type."""
        assert mermaid_renderer.supports("flowchart") is True

    def test_supports_sequence(self, mermaid_renderer):
        """Test supports for sequence diagram type."""
        assert mermaid_renderer.supports("sequencediagram") is True

    def test_supports_class(self, mermaid_renderer):
        """Test supports for class diagram type."""
        assert mermaid_renderer.supports("classdiagram") is True

    def test_supports_state(self, mermaid_renderer):
        """Test supports for state diagram type."""
        assert mermaid_renderer.supports("statediagram") is True

    def test_supports_gantt(self, mermaid_renderer):
        """Test supports for gantt diagram type."""
        assert mermaid_renderer.supports("gantt") is True

    def test_supports_unknown(self, mermaid_renderer):
        """Test supports for unknown diagram type."""
        assert mermaid_renderer.supports("unknown") is False

    def test_supports_case_insensitive(self, mermaid_renderer):
        """Test supports is case insensitive."""
        assert mermaid_renderer.supports("GRAPH") is True
        assert mermaid_renderer.supports("FlowChart") is True

    def test_render_empty_code(self, mermaid_renderer):
        """Test render with empty code."""
        result = mermaid_renderer.render("")
        assert result is None

    def test_render_not_available(self, mermaid_renderer):
        """Test render when renderer not available."""
        with patch.object(mermaid_renderer, "is_available", return_value=False):
            from markdown_book_builder.core.errors import ConfigurationError

            with pytest.raises(ConfigurationError, match="mmdc"):
                mermaid_renderer.render("graph LR\n  A --> B")

    def test_render_unsupported_type(self, mermaid_renderer):
        """Test render with unsupported diagram type."""
        with patch.object(mermaid_renderer, "is_available", return_value=True):
            result = mermaid_renderer.render("unknown LR\n  A --> B")
            assert result is None
