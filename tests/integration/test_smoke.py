"""Smoke tests for complete end-to-end workflows."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from markdown_book_builder.cli.main import app

runner = CliRunner()


@pytest.fixture
def clean_project(tmp_path: Path) -> Path:
    """Create a clean project from scratch."""
    return tmp_path / "smoke-test-project"


def test_complete_workflow(clean_project: Path) -> None:
    """Test complete workflow: init -> validate -> build."""
    assert not clean_project.exists()

    result = runner.invoke(app, ["init", str(clean_project)])
    assert result.exit_code == 0, f"Init failed: {result.stdout}"
    assert clean_project.exists()
    assert (clean_project / "book.toml").exists()
    assert (clean_project / "content").exists()

    result = runner.invoke(app, ["config", str(clean_project)])
    assert result.exit_code == 0, f"Config failed: {result.stdout}"

    result = runner.invoke(app, ["validate", str(clean_project)])
    assert result.exit_code == 0, f"Validate failed: {result.stdout}"

    with patch("markdown_book_builder.cli.build.get_renderer") as mock_get:
        mock_renderer = MagicMock()
        mock_renderer.is_available.return_value = True
        mock_renderer.render.return_value = clean_project / "output" / "book.pdf"
        mock_get.return_value = mock_renderer
        result = runner.invoke(app, ["build", str(clean_project)])
        assert result.exit_code == 0, f"Build failed: {result.stdout}"


def test_build_with_custom_chapters(tmp_path: Path) -> None:
    """Test building with custom chapter content."""
    project = tmp_path / "custom-project"
    project.mkdir()
    content = project / "content"
    content.mkdir()

    (content / "intro.md").write_text(
        """---
title: Introduction
---

# Getting Started

This is the introduction.
"""
    )

    (content / "main.md").write_text(
        """---
title: Main Content
---

# Main Section

This is the main content.

## Subsection

More details here.
"""
    )

    (project / "book.toml").write_text(
        """title = "Custom Book"
author = "Test Author"
source_dir = "content"
"""
    )

    result = runner.invoke(app, ["validate", str(project)])
    assert result.exit_code == 0

    with patch("markdown_book_builder.cli.build.get_renderer") as mock_get:
        mock_renderer = MagicMock()
        mock_renderer.is_available.return_value = True
        mock_renderer.render.return_value = project / "output" / "book.pdf"
        mock_get.return_value = mock_renderer
        result = runner.invoke(app, ["build", str(project)])
        assert result.exit_code == 0


def test_build_with_ordering(tmp_path: Path) -> None:
    """Test building with custom chapter ordering."""
    project = tmp_path / "ordered-project"
    project.mkdir()
    content = project / "content"
    content.mkdir()

    (content / "chapter_a.md").write_text("# Chapter A\nContent A")
    (content / "chapter_b.md").write_text("# Chapter B\nContent B")
    (content / "chapter_c.md").write_text("# Chapter C\nContent C")

    (project / "order.yaml").write_text(
        """order:
  - chapter_c.md
  - chapter_a.md
  - chapter_b.md
"""
    )

    (project / "book.toml").write_text(
        """title = "Ordered Book"
author = "Author"
source_dir = "content"
"""
    )

    with patch("markdown_book_builder.cli.build.get_renderer") as mock_get:
        mock_renderer = MagicMock()
        mock_renderer.is_available.return_value = True
        mock_renderer.render.return_value = project / "output" / "book.pdf"
        mock_get.return_value = mock_renderer
        result = runner.invoke(app, ["build", str(project)])
        assert result.exit_code == 0


def test_multiple_chapters_build(tmp_path: Path) -> None:
    """Test building book with multiple chapters."""
    project = tmp_path / "multi-chapter"
    project.mkdir()
    content = project / "content"
    content.mkdir()

    for i in range(5):
        (content / f"chapter{i}.md").write_text(
            f"""---
title: Chapter {i}
---

# Chapter {i}

Content for chapter {i}.
"""
        )

    (project / "book.toml").write_text(
        """title = "Multi-Chapter Book"
author = "Author"
source_dir = "content"
"""
    )

    result = runner.invoke(app, ["validate", str(project)])
    assert result.exit_code == 0, f"Validate failed: {result.stdout}"

    with patch("markdown_book_builder.cli.build.get_renderer") as mock_get:
        mock_renderer = MagicMock()
        mock_renderer.is_available.return_value = True
        mock_renderer.render.return_value = project / "output" / "book.pdf"
        mock_get.return_value = mock_renderer
        result = runner.invoke(app, ["build", str(project)])
        assert result.exit_code == 0, f"Build failed: {result.stdout}"
