"""Tests for metadata extraction."""

from pathlib import Path

import pytest

from markdown_book_builder.discovery.metadata import extract_front_matter, parse_front_matter
from tests.fixtures.discovery_samples import (
    SAMPLE_INVALID_YAML_FM,
    SAMPLE_MARKDOWN_NO_FM,
    SAMPLE_MARKDOWN_WITH_FM,
)


def test_parse_front_matter_with_fm() -> None:
    """Test parsing valid front matter."""
    meta, body = parse_front_matter(SAMPLE_MARKDOWN_WITH_FM)
    assert meta["title"] == "Chapter One"
    assert meta["author"] == "Test Author"
    assert "Introduction" in body


def test_parse_front_matter_no_fm() -> None:
    """Test parsing content without front matter."""
    meta, body = parse_front_matter(SAMPLE_MARKDOWN_NO_FM)
    assert meta == {}
    assert "Overview" in body


def test_parse_front_matter_empty() -> None:
    """Test parsing empty content."""
    meta, body = parse_front_matter("")
    assert meta == {}
    assert body == ""


def test_parse_front_matter_incomplete() -> None:
    """Test parsing incomplete front matter."""
    content = "---\ntitle: Test\nno ending delimiter"
    meta, body = parse_front_matter(content)
    assert meta == {}
    assert "---" in body


def test_parse_front_matter_invalid_yaml() -> None:
    """Test parsing invalid YAML."""
    with pytest.raises(ValueError, match="Invalid YAML"):
        parse_front_matter(SAMPLE_INVALID_YAML_FM)


def test_extract_front_matter(tmp_path: Path) -> None:
    """Test extracting front matter from file."""
    file_path = tmp_path / "test.md"
    file_path.write_text(SAMPLE_MARKDOWN_WITH_FM)

    fm = extract_front_matter(file_path)
    assert fm.title == "Chapter One"
    assert fm.author == "Test Author"
    assert fm.date == "2026-07-13"


def test_extract_front_matter_no_fm(tmp_path: Path) -> None:
    """Test extracting when no front matter exists."""
    file_path = tmp_path / "test.md"
    file_path.write_text(SAMPLE_MARKDOWN_NO_FM)

    fm = extract_front_matter(file_path)
    assert fm.title is None
    assert fm.author is None


def test_extract_front_matter_not_found() -> None:
    """Test error on non-existent file."""
    with pytest.raises(FileNotFoundError):
        extract_front_matter(Path("/nonexistent/file.md"))


def test_parse_front_matter_with_extra_fields() -> None:
    """Test parsing front matter with extra fields."""
    content = """---
title: Test
author: Author
custom_field: custom_value
another: 42
---

# Content
"""
    meta, _ = parse_front_matter(content)
    assert meta["title"] == "Test"
    assert meta["custom_field"] == "custom_value"
    assert meta["another"] == 42
