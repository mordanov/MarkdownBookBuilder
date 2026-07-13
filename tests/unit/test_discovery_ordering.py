"""Tests for chapter ordering."""

from pathlib import Path

import pytest

from markdown_book_builder.discovery.ordering import load_order_config, sort_chapters
from tests.fixtures.discovery_samples import SAMPLE_ORDER_YAML


def test_load_order_config(tmp_path: Path) -> None:
    """Test loading order configuration."""
    order_file = tmp_path / "order.yaml"
    order_file.write_text(SAMPLE_ORDER_YAML)

    order = load_order_config(order_file)
    assert order == ["chapter1.md", "chapter2.md", "chapter3.md"]


def test_load_order_config_empty(tmp_path: Path) -> None:
    """Test loading empty order config."""
    order_file = tmp_path / "order.yaml"
    order_file.write_text("# No order section\n")

    order = load_order_config(order_file)
    assert order == []


def test_load_order_config_not_found() -> None:
    """Test error on missing order file."""
    with pytest.raises(FileNotFoundError):
        load_order_config(Path("/nonexistent/order.yaml"))


def test_load_order_config_invalid_yaml(tmp_path: Path) -> None:
    """Test error on invalid YAML."""
    order_file = tmp_path / "order.yaml"
    order_file.write_text("order:\n  - item1\n    invalid: yaml: here")

    with pytest.raises(ValueError, match="Invalid YAML"):
        load_order_config(order_file)


def test_sort_chapters_with_order() -> None:
    """Test sorting with explicit order."""
    files = [
        Path("chapter3.md"),
        Path("chapter1.md"),
        Path("chapter2.md"),
    ]
    order = ["chapter1.md", "chapter2.md", "chapter3.md"]

    result = sort_chapters(files, order)
    assert [f.name for f in result] == ["chapter1.md", "chapter2.md", "chapter3.md"]


def test_sort_chapters_partial_order() -> None:
    """Test sorting when order doesn't include all files."""
    files = [
        Path("chapter3.md"),
        Path("chapter1.md"),
        Path("chapter2.md"),
        Path("chapter4.md"),
    ]
    order = ["chapter1.md", "chapter2.md"]

    result = sort_chapters(files, order)
    assert result[0].name == "chapter1.md"
    assert result[1].name == "chapter2.md"
    assert {f.name for f in result} == {
        "chapter1.md",
        "chapter2.md",
        "chapter3.md",
        "chapter4.md",
    }


def test_sort_chapters_no_order() -> None:
    """Test sorting without order (alphabetical)."""
    files = [
        Path("chapter3.md"),
        Path("chapter1.md"),
        Path("chapter2.md"),
    ]

    result = sort_chapters(files, None)
    assert [f.name for f in result] == ["chapter1.md", "chapter2.md", "chapter3.md"]


def test_sort_chapters_empty() -> None:
    """Test sorting empty list."""
    result = sort_chapters([], None)
    assert result == []


def test_sort_chapters_nonexistent_in_order() -> None:
    """Test order with nonexistent files."""
    files = [Path("b.md"), Path("a.md")]
    order = ["c.md", "a.md", "b.md"]

    result = sort_chapters(files, order)
    assert result[0].name == "a.md"
    assert result[1].name == "b.md"
