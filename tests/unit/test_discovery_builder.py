"""Tests for AST builder from Markdown files."""

from pathlib import Path

import pytest

from markdown_book_builder.ast_.models import Book
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.discovery.builder import build_ast_from_files, parse_markdown_file
from tests.fixtures.discovery_samples import (
    MARKDOWN_WITH_MULTIPLE_HEADINGS,
    SAMPLE_MARKDOWN_NO_FM,
    SAMPLE_MARKDOWN_WITH_FM,
)


@pytest.fixture
def sample_config() -> BookConfig:
    """Sample book configuration."""
    return BookConfig(
        title="Test Book",
        author="Test Author",
        version="1.0.0",
    )


def test_parse_markdown_file_with_fm(tmp_path: Path) -> None:
    """Test parsing file with front matter."""
    file_path = tmp_path / "chapter.md"
    file_path.write_text(SAMPLE_MARKDOWN_WITH_FM)

    chapter = parse_markdown_file(file_path)
    assert chapter.title == "Chapter One"
    assert len(chapter.children) >= 1


def test_parse_markdown_file_no_fm(tmp_path: Path) -> None:
    """Test parsing file without front matter."""
    file_path = tmp_path / "chapter.md"
    file_path.write_text(SAMPLE_MARKDOWN_NO_FM)

    chapter = parse_markdown_file(file_path)
    assert chapter.title == "chapter"
    assert len(chapter.children) >= 1


def test_parse_markdown_file_multiple_headings(tmp_path: Path) -> None:
    """Test parsing file with multiple heading levels."""
    file_path = tmp_path / "complex.md"
    file_path.write_text(MARKDOWN_WITH_MULTIPLE_HEADINGS)

    chapter = parse_markdown_file(file_path)
    assert chapter.title == "Multi Heading"
    assert len(chapter.children) >= 2


def test_parse_markdown_file_not_found() -> None:
    """Test error on non-existent file."""
    with pytest.raises(FileNotFoundError):
        parse_markdown_file(Path("/nonexistent/file.md"))


def test_build_ast_from_files(tmp_path: Path, sample_config: BookConfig) -> None:
    """Test building AST from multiple files."""
    (tmp_path / "ch1.md").write_text("---\ntitle: Chapter 1\n---\n# Intro\nContent")
    (tmp_path / "ch2.md").write_text("---\ntitle: Chapter 2\n---\n# Overview\nContent")

    files = sorted(tmp_path.glob("*.md"))
    book = build_ast_from_files(files, sample_config)

    assert isinstance(book, Book)
    assert book.title == "Test Book"
    assert book.author == "Test Author"
    assert len(book.chapters) == 2


def test_build_ast_from_files_empty(sample_config: BookConfig) -> None:
    """Test error on empty file list."""
    with pytest.raises(ValueError, match="No Markdown files"):
        build_ast_from_files([], sample_config)


def test_build_ast_preserves_order(tmp_path: Path, sample_config: BookConfig) -> None:
    """Test that file order is preserved in AST."""
    (tmp_path / "first.md").write_text("---\ntitle: First\n---\n# First")
    (tmp_path / "second.md").write_text("---\ntitle: Second\n---\n# Second")
    (tmp_path / "third.md").write_text("---\ntitle: Third\n---\n# Third")

    files = [
        tmp_path / "first.md",
        tmp_path / "second.md",
        tmp_path / "third.md",
    ]

    book = build_ast_from_files(files, sample_config)
    assert book.chapters[0].title == "First"
    assert book.chapters[1].title == "Second"
    assert book.chapters[2].title == "Third"
