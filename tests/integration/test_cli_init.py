"""Integration tests for init command."""

from pathlib import Path

from typer.testing import CliRunner

from markdown_book_builder.cli.main import app

runner = CliRunner()


def test_init_creates_project(tmp_path: Path) -> None:
    """Test init creates project structure."""
    project_path = tmp_path / "new-book"

    result = runner.invoke(app, ["init", str(project_path)])
    assert result.exit_code == 0
    assert "initialized" in result.stdout.lower()

    assert project_path.exists()
    assert (project_path / "book.toml").exists()
    assert (project_path / "README.md").exists()
    assert (project_path / "content").is_dir()
    assert (project_path / "order.yaml").exists()


def test_init_creates_sample_chapters(tmp_path: Path) -> None:
    """Test init creates sample chapter files."""
    project_path = tmp_path / "new-book"

    result = runner.invoke(app, ["init", str(project_path)])
    assert result.exit_code == 0

    content_dir = project_path / "content"
    assert (content_dir / "chapter1.md").exists()
    assert (content_dir / "chapter2.md").exists()

    ch1 = (content_dir / "chapter1.md").read_text()
    assert "Introduction" in ch1
    assert "---" in ch1  # Has front matter


def test_init_valid_toml(tmp_path: Path) -> None:
    """Test init creates valid book.toml."""
    project_path = tmp_path / "new-book"

    result = runner.invoke(app, ["init", str(project_path)])
    assert result.exit_code == 0

    toml_content = (project_path / "book.toml").read_text()
    assert "title" in toml_content
    assert "author" in toml_content
    assert "source_dir" in toml_content
    assert "[output]" in toml_content


def test_init_valid_readme(tmp_path: Path) -> None:
    """Test init creates comprehensive README."""
    project_path = tmp_path / "new-book"

    result = runner.invoke(app, ["init", str(project_path)])
    assert result.exit_code == 0

    readme = (project_path / "README.md").read_text()
    assert "markdown-book-builder" in readme.lower()
    assert "content/" in readme


def test_init_existing_path(tmp_path: Path) -> None:
    """Test init fails on existing path."""
    project_path = tmp_path / "existing"
    project_path.mkdir()

    result = runner.invoke(app, ["init", str(project_path)])
    assert result.exit_code != 0
    assert "already exists" in result.stdout


def test_init_creates_nested_structure(tmp_path: Path) -> None:
    """Test init creates nested directory structure."""
    project_path = tmp_path / "a" / "b" / "new-book"

    result = runner.invoke(app, ["init", str(project_path)])
    assert result.exit_code == 0
    assert project_path.exists()
    assert (project_path / "content").exists()
