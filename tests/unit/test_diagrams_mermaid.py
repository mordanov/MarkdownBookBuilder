"""Tests for Mermaid diagram rendering."""

import pytest

from markdown_book_builder.core.errors import ConfigurationError
from markdown_book_builder.diagrams.mermaid import render_mermaid, validate_mermaid


def test_validate_mermaid_graph() -> None:
    """Test validating graph diagram."""
    code = """graph TD
    A --> B
    B --> C"""

    assert validate_mermaid(code) is True


def test_validate_mermaid_flowchart() -> None:
    """Test validating flowchart diagram."""
    code = """flowchart LR
    Start --> Process
    Process --> End"""

    assert validate_mermaid(code) is True


def test_validate_mermaid_sequence() -> None:
    """Test validating sequence diagram."""
    code = """sequenceDiagram
    participant A
    participant B
    A->>B: Hello"""

    assert validate_mermaid(code) is True


def test_validate_mermaid_invalid() -> None:
    """Test validating invalid diagram."""
    code = "This is not a diagram"
    assert validate_mermaid(code) is False


def test_validate_mermaid_empty() -> None:
    """Test validating empty diagram."""
    assert validate_mermaid("") is False
    assert validate_mermaid("   ") is False


def test_render_mermaid_missing_cli() -> None:
    """Test rendering without mermaid-cli installed."""
    code = "graph TD\nA --> B"

    with pytest.raises(ConfigurationError) as exc_info:
        render_mermaid(code)

    assert "mermaid-cli" in str(exc_info.value).lower()


def test_render_mermaid_invalid_code() -> None:
    """Test rendering invalid diagram raises error when mmdc not available."""
    code = "this is not valid mermaid"

    with pytest.raises(ConfigurationError) as exc_info:
        render_mermaid(code)

    assert "mermaid" in str(exc_info.value).lower()
