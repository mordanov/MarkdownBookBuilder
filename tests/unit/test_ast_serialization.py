"""Snapshot tests for AST serialization/deserialization."""

import json

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text


def test_ast_roundtrip_simple() -> None:
    """Test that AST can be serialized and deserialized with fidelity."""
    text = Text(content="Hello world")
    para = Paragraph(children=[text])
    sec = Section(title="Section 1", level=1, children=[para])
    ch = Chapter(title="Chapter 1", children=[sec])
    book = Book(title="Test Book", author="Test Author", chapters=[ch])

    serialized = book.model_dump_json()
    deserialized = Book.model_validate_json(serialized)

    assert deserialized.title == book.title
    assert deserialized.author == book.author
    assert len(deserialized.chapters) == 1
    assert deserialized.chapters[0].title == "Chapter 1"


def test_ast_roundtrip_complex() -> None:
    """Test complex nested AST structure preserves all data."""
    from markdown_book_builder.ast_.models import CodeBlock, Image

    code = CodeBlock(language="python", content="x = 1", line_numbers=True)
    img = Image(path="img.png", alt_text="Image", caption="Caption", width="200px")
    text1 = Text(content="Text before ")
    text2 = Text(content=" text after")

    para = Paragraph(children=[text1, code, text2, img])
    sec = Section(title="Complex", level=2, children=[para])
    ch = Chapter(title="Ch", number=1, children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    data = book.model_dump()
    restored = Book(**data)

    assert restored == book
    section = restored.chapters[0].children[0]
    assert isinstance(section, Section)
    para = section.children[0]
    assert isinstance(para, Paragraph)
    assert len(para.children) == 4


def test_ast_to_dict() -> None:
    """Test AST converts to dict correctly."""
    text = Text(content="Test")
    para = Paragraph(children=[text])
    book = Book(title="Book", author="Author")

    data = book.model_dump()
    assert isinstance(data, dict)
    assert data["title"] == "Book"
    assert "chapters" in data


def test_ast_to_json() -> None:
    """Test AST converts to JSON correctly."""
    text = Text(content="Test")
    book = Book(title="Book", author="Author")

    json_str = book.model_dump_json()
    assert isinstance(json_str, str)
    assert "Book" in json_str

    parsed = json.loads(json_str)
    assert parsed["title"] == "Book"
