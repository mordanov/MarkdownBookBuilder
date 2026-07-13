"""Tests for AST transformation utilities."""

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.ast_.transform import (
    count_nodes,
    find_all_sections,
    get_headings,
    traverse_ast,
)


def test_traverse_ast_simple() -> None:
    """Test traversing a simple AST."""
    text = Text(content="Hello")
    para = Paragraph(children=[text])
    sec = Section(title="S1", level=1, children=[para])
    ch = Chapter(title="C1", children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    nodes = list(traverse_ast(book))
    assert len(nodes) > 0
    assert any(isinstance(n, Text) for n in nodes)


def test_traverse_ast_deeply_nested() -> None:
    """Test traversing deeply nested AST (10+ levels)."""
    sections = []
    for i in range(10):
        sec = Section(title=f"Level {i}", level=(i % 6) + 1)
        sections.append(sec)

    ch = Chapter(title="Ch", children=sections)
    book = Book(title="Book", author="Author", chapters=[ch])

    nodes = list(traverse_ast(book))
    assert len(nodes) >= 10


def test_find_all_sections() -> None:
    """Test finding all sections in AST."""
    sec1 = Section(title="S1", level=1)
    sec2 = Section(title="S2", level=2)
    ch = Chapter(title="C1", children=[sec1, sec2])
    book = Book(title="Book", author="Author", chapters=[ch])

    sections = find_all_sections(book)
    assert len(sections) >= 2


def test_count_nodes() -> None:
    """Test counting all nodes of specific types."""
    text1 = Text(content="T1")
    text2 = Text(content="T2")
    para = Paragraph(children=[text1, text2])
    sec = Section(title="S", level=1, children=[para])
    ch = Chapter(title="C", children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    text_count = count_nodes(book, Text)
    assert text_count >= 2


def test_get_headings() -> None:
    """Test extracting all headings from AST."""
    sec1 = Section(title="Introduction", level=1)
    sec2 = Section(title="Background", level=2)
    ch = Chapter(title="Chapter One", children=[sec1, sec2])
    book = Book(title="Book", author="Author", chapters=[ch])

    headings = get_headings(book)
    assert any("Introduction" in str(h) for h in headings)


def test_traverse_preserves_structure() -> None:
    """Test that traversal doesn't modify the AST."""
    text = Text(content="Original")
    para = Paragraph(children=[text])
    sec = Section(title="Sec", level=1, children=[para])
    ch = Chapter(title="Ch", children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    original_title = book.chapters[0].title
    list(traverse_ast(book))

    assert book.chapters[0].title == original_title
