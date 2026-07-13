"""Integration tests for config command."""

from pathlib import Path

import pytest
from typer.testing import CliRunner

from markdown_book_builder.cli.main import app

runner = CliRunner()


@pytest.fixture
def config_project(tmp_path: Path) -> Path:
    """Create a project with configuration."""
    project = tmp_path / "config-test"
    project.mkdir()

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
    return project


def test_config_displays_settings(config_project: Path) -> None:
    """Test config command displays settings."""
    result = runner.invoke(app, ["config", str(config_project)])
    assert result.exit_code == 0

    output = result.stdout
    assert "Test Book" in output
    assert "Test Author" in output
    assert "1.0.0" in output
    assert "pdf" in output


def test_config_from_toml_file(config_project: Path) -> None:
    """Test config with explicit toml file."""
    toml_file = config_project / "book.toml"
    result = runner.invoke(app, ["config", str(toml_file)])
    assert result.exit_code == 0
    assert "Configuration valid" in result.stdout or "✓" in result.stdout


def test_config_shows_openai_model(config_project: Path) -> None:
    """Test config displays OpenAI model."""
    result = runner.invoke(app, ["config", str(config_project)])
    assert result.exit_code == 0
    assert "gpt-4o" in result.stdout


def test_config_nonexistent_path() -> None:
    """Test config with non-existent path."""
    result = runner.invoke(app, ["config", "/nonexistent"])
    assert result.exit_code != 0


def test_config_missing_toml(tmp_path: Path) -> None:
    """Test config without book.toml."""
    project = tmp_path / "no-config"
    project.mkdir()
    result = runner.invoke(app, ["config", str(project)])
    assert result.exit_code != 0
