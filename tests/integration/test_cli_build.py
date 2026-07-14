"""Integration tests for build command."""

from collections.abc import Generator
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from markdown_book_builder.cli.main import app

runner = CliRunner()


@pytest.fixture
def sample_project(tmp_path: Path) -> Generator[Path]:
    """Create a sample book project."""
    project = tmp_path / "sample-book"
    project.mkdir()

    content_dir = project / "content"
    content_dir.mkdir()

    (content_dir / "chapter1.md").write_text(
        """---
title: Chapter One
---

# Introduction

This is the introduction.
"""
    )

    (content_dir / "chapter2.md").write_text(
        """---
title: Chapter Two
---

# Details

These are the details.
"""
    )

    book_toml = """title = "Test Book"
author = "Test Author"
version = "1.0.0"
source_dir = "content"

[output]
format = "pdf"
path = "output/book.pdf"

[openai]
model = "gpt-4o"
"""
    (project / "book.toml").write_text(book_toml)

    yield project


def test_build_from_directory(sample_project: Path) -> None:
    """Test build command from directory."""
    with patch("markdown_book_builder.cli.build.get_renderer") as mock_get:
        mock_renderer = MagicMock()
        mock_renderer.is_available.return_value = True
        mock_renderer.render.return_value = sample_project / "output" / "book.pdf"
        mock_get.return_value = mock_renderer
        result = runner.invoke(app, ["build", str(sample_project)])
        assert result.exit_code == 0
        assert "Build complete" in result.stdout
        assert "PDF written to" in result.stdout


def test_build_from_toml_file(sample_project: Path) -> None:
    """Test build command with explicit toml file."""
    with patch("markdown_book_builder.cli.build.get_renderer") as mock_get:
        mock_renderer = MagicMock()
        mock_renderer.is_available.return_value = True
        mock_renderer.render.return_value = sample_project / "output" / "book.pdf"
        mock_get.return_value = mock_renderer
        toml_file = sample_project / "book.toml"
        result = runner.invoke(app, ["build", str(toml_file)])
        assert result.exit_code == 0


def test_build_nonexistent_path() -> None:
    """Test build with non-existent path."""
    result = runner.invoke(app, ["build", "/nonexistent/path"])
    assert result.exit_code != 0
    assert "not a valid path" in result.stdout


def test_build_missing_config(tmp_path: Path) -> None:
    """Test build without book.toml."""
    project = tmp_path / "no-config"
    project.mkdir()
    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0


def test_build_no_markdown_files(tmp_path: Path) -> None:
    """Test build with no Markdown files."""
    project = tmp_path / "empty-project"
    project.mkdir()
    (project / "content").mkdir()

    book_toml = """title = "Empty"
author = "Author"
source_dir = "content"
"""
    (project / "book.toml").write_text(book_toml)

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0
    assert "No Markdown files" in result.stdout or "not found" in result.stdout.lower()


def test_build_with_full_formatting_config(tmp_path: Path) -> None:
    """Build succeeds when book.toml contains a full [formatting] section."""
    project = tmp_path / "formatted-book"
    project.mkdir()
    content = project / "content"
    content.mkdir()
    (content / "ch1.md").write_text("# Chapter One\n\nSome text.\n")

    book_toml = """title = "Formatted Book"
author = "Author"
source_dir = "content"

[output]
format = "pdf"
path = "output/book.pdf"

[formatting.page]
paper_size = "a4"
margin_top = "2cm"
margin_bottom = "2cm"
margin_left = "3cm"
margin_right = "2cm"

[formatting.toc]
enabled = true
depth = 3
interactive = true

[formatting.headings.h1]
font_size = 24
bold = true
color = "#FFFFFF"
background = "#003366"

[formatting.headings.h2]
font_size = 18
bold = true
color = "#003366"
"""
    (project / "book.toml").write_text(book_toml)

    with patch("markdown_book_builder.cli.build.get_renderer") as mock_get:
        mock_renderer = MagicMock()
        mock_renderer.is_available.return_value = True
        mock_renderer.render.return_value = project / "output" / "book.pdf"
        mock_get.return_value = mock_renderer

        result = runner.invoke(app, ["build", str(project)])

    assert result.exit_code == 0, result.stdout


def test_build_invalid_hex_color_exits_nonzero(tmp_path: Path) -> None:
    """Build exits with non-zero code when an invalid HEX color is in book.toml."""
    project = tmp_path / "invalid-color-book"
    project.mkdir()
    content = project / "content"
    content.mkdir()
    (content / "ch1.md").write_text("# Chapter\n\nText.\n")

    book_toml = """title = "Bad Color Book"
author = "Author"
source_dir = "content"

[formatting.headings.h1]
font_size = 22
color = "#ZZZZZZ"
"""
    (project / "book.toml").write_text(book_toml)

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0
