"""Error scenario and edge case tests."""

from pathlib import Path

from typer.testing import CliRunner

from markdown_book_builder.cli.main import app

runner = CliRunner()


def test_build_nonexistent_directory() -> None:
    """Test building non-existent directory."""
    result = runner.invoke(app, ["build", "/nonexistent/path/to/project"])
    assert result.exit_code != 0


def test_build_without_config(tmp_path: Path) -> None:
    """Test building without book.toml."""
    project = tmp_path / "no-config"
    project.mkdir()
    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0


def test_build_with_invalid_toml(tmp_path: Path) -> None:
    """Test building with malformed TOML."""
    project = tmp_path / "invalid-toml"
    project.mkdir()

    (project / "book.toml").write_text("""
title = "Invalid
this is broken TOML
""")

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0


def test_build_with_missing_title(tmp_path: Path) -> None:
    """Test building with missing required field."""
    project = tmp_path / "no-title"
    project.mkdir()
    (project / "content").mkdir()

    (project / "book.toml").write_text("""
author = "Author"
source_dir = "content"
""")

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0


def test_build_with_missing_author(tmp_path: Path) -> None:
    """Test building with missing author."""
    project = tmp_path / "no-author"
    project.mkdir()
    (project / "content").mkdir()

    (project / "book.toml").write_text("""
title = "Title"
source_dir = "content"
""")

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0


def test_build_empty_content_directory(tmp_path: Path) -> None:
    """Test building with empty content directory."""
    project = tmp_path / "empty-content"
    project.mkdir()
    (project / "content").mkdir()

    (project / "book.toml").write_text("""
title = "Empty Book"
author = "Author"
source_dir = "content"
""")

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0
    assert "No Markdown files" in result.stdout or "not found" in result.stdout.lower()


def test_init_existing_project(tmp_path: Path) -> None:
    """Test init fails on existing directory."""
    project = tmp_path / "existing"
    project.mkdir()

    result = runner.invoke(app, ["init", str(project)])
    assert result.exit_code != 0


def test_validate_missing_source_dir(tmp_path: Path) -> None:
    """Test validate when source_dir doesn't exist."""
    project = tmp_path / "missing-source"
    project.mkdir()

    (project / "book.toml").write_text("""
title = "Test"
author = "Author"
source_dir = "nonexistent_dir"
""")

    result = runner.invoke(app, ["validate", str(project)])
    assert result.exit_code != 0


def test_config_invalid_toml(tmp_path: Path) -> None:
    """Test config command with invalid TOML."""
    project = tmp_path / "bad-config"
    project.mkdir()

    (project / "book.toml").write_text("""
invalid toml: structure
title = [unclosed array
""")

    result = runner.invoke(app, ["config", str(project)])
    assert result.exit_code != 0


def test_invalid_source_dir_value(tmp_path: Path) -> None:
    """Test with invalid source_dir configuration."""
    project = tmp_path / "invalid-source"
    project.mkdir()
    (project / "content").mkdir()

    (project / "book.toml").write_text("""
title = "Test"
author = "Author"
source_dir = ""
""")

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0


def test_build_with_only_non_markdown_files(tmp_path: Path) -> None:
    """Test building with only non-markdown files."""
    project = tmp_path / "no-markdown"
    project.mkdir()
    content = project / "content"
    content.mkdir()

    (content / "readme.txt").write_text("Not markdown")
    (content / "data.json").write_text("{}")

    (project / "book.toml").write_text("""
title = "Test"
author = "Author"
source_dir = "content"
""")

    result = runner.invoke(app, ["build", str(project)])
    assert result.exit_code != 0
