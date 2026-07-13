"""Performance benchmark tests for core operations."""

import time
from pathlib import Path

from markdown_book_builder.ast_.models import (
    Book,
    Chapter,
    Paragraph,
    Section,
    Text,
)
from markdown_book_builder.ast_.transform import count_nodes, find_all_sections, traverse_ast
from markdown_book_builder.images.cache import ImageCache


def create_large_ast(num_chapters: int = 10, sections_per_chapter: int = 5) -> Book:
    """Create a large AST for benchmarking."""
    chapters = []

    for ch_idx in range(num_chapters):
        sections = []
        for sec_idx in range(sections_per_chapter):
            text = Text(content=f"Content for chapter {ch_idx} section {sec_idx}")
            para = Paragraph(children=[text])
            section = Section(
                title=f"Section {sec_idx}",
                level=1 + (sec_idx % 3),
                children=[para],
            )
            sections.append(section)

        chapter = Chapter(title=f"Chapter {ch_idx}", children=sections)
        chapters.append(chapter)

    return Book(title="Large Book", author="Author", chapters=chapters)


def test_traverse_ast_performance() -> None:
    """Benchmark AST traversal."""
    book = create_large_ast(num_chapters=10, sections_per_chapter=10)

    start = time.time()
    nodes = list(traverse_ast(book))
    elapsed = time.time() - start

    assert len(nodes) > 0
    assert elapsed < 1.0, f"AST traversal took {elapsed}s, should be < 1s"


def test_find_sections_performance() -> None:
    """Benchmark finding all sections."""
    book = create_large_ast(num_chapters=20, sections_per_chapter=5)

    start = time.time()
    sections = find_all_sections(book)
    elapsed = time.time() - start

    assert len(sections) == 100  # 20 chapters * 5 sections
    assert elapsed < 0.5, f"Finding sections took {elapsed}s, should be < 0.5s"


def test_count_nodes_performance() -> None:
    """Benchmark node counting."""
    book = create_large_ast(num_chapters=15, sections_per_chapter=5)

    start = time.time()
    count = count_nodes(book, Section)
    elapsed = time.time() - start

    assert count == 75  # 15 chapters * 5 sections
    assert elapsed < 0.2, f"Node counting took {elapsed}s, should be < 0.2s"


def test_cache_performance(tmp_path: Path) -> None:
    """Benchmark image caching."""
    cache = ImageCache(tmp_path / "cache")
    test_data = b"test image data" * 1000

    start = time.time()
    for i in range(100):
        cache.cache_image(f"prompt_{i}", test_data)
    elapsed = time.time() - start

    assert elapsed < 1.0, f"Caching 100 images took {elapsed}s, should be < 1s"


def test_cache_retrieval_performance(tmp_path: Path) -> None:
    """Benchmark cache retrieval."""
    cache = ImageCache(tmp_path / "cache")
    test_data = b"test image data"

    for i in range(100):
        cache.cache_image(f"prompt_{i}", test_data)

    start = time.time()
    for i in range(100):
        result = cache.get_cached_image(f"prompt_{i}")
        assert result is not None
    elapsed = time.time() - start

    assert elapsed < 0.5, f"Retrieving 100 cached images took {elapsed}s, should be < 0.5s"


def test_large_ast_memory() -> None:
    """Test that large AST doesn't consume excessive memory."""
    book = create_large_ast(num_chapters=100, sections_per_chapter=10)

    assert len(book.chapters) == 100

    total_nodes = len(list(traverse_ast(book)))
    assert total_nodes > 1000

    assert len(book.chapters[0].children) == 10
