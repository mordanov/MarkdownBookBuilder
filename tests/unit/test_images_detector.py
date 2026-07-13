"""Tests for image placeholder detection."""

from markdown_book_builder.ast_.models import Book, Chapter, Image, Paragraph, Section, Text
from markdown_book_builder.images.detector import detect_placeholders, find_mermaid_diagrams


def test_detect_no_placeholders() -> None:
    """Test detecting book with no images."""
    text = Text(content="Hello")
    para = Paragraph(children=[text])
    sec = Section(title="Intro", level=1, children=[para])
    ch = Chapter(title="Ch1", children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    placeholders = detect_placeholders(book)
    assert len(placeholders) == 0


def test_detect_single_placeholder() -> None:
    """Test detecting single image."""
    img = Image(path="pic.png", alt_text="Picture")
    para = Paragraph(children=[img])
    sec = Section(title="Intro", level=1, children=[para])
    ch = Chapter(title="Ch1", children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    placeholders = detect_placeholders(book)
    assert len(placeholders) == 1
    assert placeholders[0].alt_text == "Picture"
    assert placeholders[0].path == "pic.png"


def test_detect_multiple_placeholders() -> None:
    """Test detecting multiple images."""
    img1 = Image(path="pic1.png", alt_text="First")
    img2 = Image(path="pic2.png", alt_text="Second")
    para = Paragraph(children=[img1, img2])
    sec = Section(title="Intro", level=1, children=[para])
    ch = Chapter(title="Ch1", children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    placeholders = detect_placeholders(book)
    assert len(placeholders) == 2
    assert placeholders[0].alt_text == "First"
    assert placeholders[1].alt_text == "Second"


def test_detect_with_caption() -> None:
    """Test detecting image with caption."""
    img = Image(path="pic.png", alt_text="Alt", caption="This is a caption")
    para = Paragraph(children=[img])
    sec = Section(title="Intro", level=1, children=[para])
    ch = Chapter(title="Ch1", children=[sec])
    book = Book(title="Book", author="Author", chapters=[ch])

    placeholders = detect_placeholders(book)
    assert len(placeholders) == 1
    assert placeholders[0].caption == "This is a caption"


def test_find_mermaid_diagrams() -> None:
    """Test finding sections with diagrams."""
    sec1 = Section(title="Normal Section", level=1)
    sec2 = Section(title="Diagram: Flow", level=1)
    sec3 = Section(title="Another Diagram", level=1)

    ch = Chapter(title="Ch1", children=[sec1, sec2, sec3])
    book = Book(title="Book", author="Author", chapters=[ch])

    diagrams = find_mermaid_diagrams(book)
    assert len(diagrams) >= 1
    assert any("diagram" in d.lower() for d in diagrams)


def test_detect_deeply_nested() -> None:
    """Test detecting images in deeply nested structure."""
    img = Image(path="deep.png", alt_text="Deep")
    para = Paragraph(children=[img])
    sec1 = Section(title="S1", level=1, children=[para])
    sec2 = Section(title="S2", level=2, children=[sec1])
    ch = Chapter(title="Ch1", children=[sec2])
    book = Book(title="Book", author="Author", chapters=[ch])

    placeholders = detect_placeholders(book)
    assert len(placeholders) == 1
