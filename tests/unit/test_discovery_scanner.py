"""Tests for document scanner."""

from pathlib import Path

import pytest

from markdown_book_builder.discovery.scanner import scan_directory


@pytest.fixture
def temp_md_structure(tmp_path: Path) -> Path:
    """Create temporary Markdown file structure."""
    (tmp_path / "chapter1.md").write_text("# Chapter 1\nContent")
    (tmp_path / "chapter2.md").write_text("# Chapter 2\nContent")

    subdir = tmp_path / "part1"
    subdir.mkdir()
    (subdir / "chapter3.md").write_text("# Chapter 3\nContent")
    (subdir / "chapter4.md").write_text("# Chapter 4\nContent")

    (tmp_path / "readme.txt").write_text("Not markdown")

    return tmp_path


def test_scan_directory_recursive(temp_md_structure: Path) -> None:
    """Test recursive directory scanning."""
    files = scan_directory(temp_md_structure, recursive=True)
    assert len(files) == 4
    assert all(f.suffix == ".md" for f in files)


def test_scan_directory_non_recursive(temp_md_structure: Path) -> None:
    """Test non-recursive scanning."""
    files = scan_directory(temp_md_structure, recursive=False)
    assert len(files) == 2
    assert all(f.name.startswith("chapter") for f in files)


def test_scan_directory_sorted(temp_md_structure: Path) -> None:
    """Test files are sorted."""
    files = scan_directory(temp_md_structure, recursive=True, sort=True)
    sorted_files = sorted(files)
    assert files == sorted_files


def test_scan_directory_unsorted(temp_md_structure: Path) -> None:
    """Test unsorted result."""
    files = scan_directory(temp_md_structure, recursive=True, sort=False)
    assert len(files) == 4


def test_scan_directory_not_found() -> None:
    """Test error on non-existent directory."""
    with pytest.raises(FileNotFoundError):
        scan_directory("/nonexistent/path")


def test_scan_directory_empty(tmp_path: Path) -> None:
    """Test scanning empty directory."""
    files = scan_directory(tmp_path)
    assert files == []


def test_scan_directory_nested_deep(tmp_path: Path) -> None:
    """Test deeply nested directory structure."""
    (tmp_path / "a" / "b" / "c").mkdir(parents=True)
    (tmp_path / "a" / "b" / "c" / "deep.md").write_text("# Deep")

    files = scan_directory(tmp_path, recursive=True)
    assert len(files) == 1
    assert files[0].name == "deep.md"


def test_scan_returns_absolute_paths(temp_md_structure: Path) -> None:
    """Test that returned paths are absolute."""
    files = scan_directory(temp_md_structure)
    assert all(f.is_absolute() for f in files)
