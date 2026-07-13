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
