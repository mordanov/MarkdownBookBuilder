"""Integration tests for validate command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from markdown_book_builder.cli.main import app

runner = CliRunner()


@pytest.fixture
def valid_project(tmp_path: Path) -> Path:
    """Create a valid book project."""
    project = tmp_path / "valid"
    project.mkdir()

    content_dir = project / "content"
    content_dir.mkdir()

    (content_dir / "ch1.md").write_text("---\ntitle: Chapter\n---\n# Intro\nContent")

    book_toml = """title = "Valid"
author = "Author"
source_dir = "content"
"""
    (project / "book.toml").write_text(book_toml)

    return project


def test_validate_valid_project(valid_project: Path) -> None:
    """Test validate with valid project."""
    result = runner.invoke(app, ["validate", str(valid_project)])
    assert result.exit_code == 0
    assert "Validation passed" in result.stdout or "✓" in result.stdout


def test_validate_from_toml(valid_project: Path) -> None:
    """Test validate with explicit toml file."""
    toml_file = valid_project / "book.toml"
    result = runner.invoke(app, ["validate", str(toml_file)])
    assert result.exit_code == 0


def test_validate_nonexistent_path() -> None:
    """Test validate with non-existent path."""
    result = runner.invoke(app, ["validate", "/nonexistent"])
    assert result.exit_code != 0


def test_validate_no_markdown(tmp_path: Path) -> None:
    """Test validate with no Markdown files."""
    project = tmp_path / "no-md"
    project.mkdir()
    (project / "content").mkdir()

    book_toml = """title = "Test"
author = "Author"
source_dir = "content"
"""
    (project / "book.toml").write_text(book_toml)

    result = runner.invoke(app, ["validate", str(project)])
    assert result.exit_code != 0
