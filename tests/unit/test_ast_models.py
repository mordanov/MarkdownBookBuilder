"""Unit tests for AST models."""

import pytest
from pydantic import ValidationError

from markdown_book_builder.ast_.models import (
    Book,
    Chapter,
    CodeBlock,
    FrontMatter,
    Image,
    Paragraph,
    Section,
    Text,
)


class TestText:
    def test_text_creation(self) -> None:
        text = Text(content="Hello")
        assert text.content == "Hello"

    def test_text_empty_content(self) -> None:
        text = Text(content="")
        assert text.content == ""

    def test_text_unicode(self) -> None:
        text = Text(content="你好世界 🚀")
        assert "你好" in text.content


class TestCodeBlock:
    def test_code_block_with_language(self) -> None:
        code = CodeBlock(language="python", content="print('hi')")
        assert code.language == "python"
        assert code.content == "print('hi')"

    def test_code_block_no_language(self) -> None:
        code = CodeBlock(content="plain text")
        assert code.language is None

    def test_code_block_line_numbers(self) -> None:
        code = CodeBlock(language="js", content="const x = 1;", line_numbers=True)
        assert code.line_numbers is True


class TestImage:
    def test_image_required_fields(self) -> None:
        img = Image(path="pic.png", alt_text="Picture")
        assert img.path == "pic.png"
        assert img.alt_text == "Picture"

    def test_image_with_caption(self) -> None:
        img = Image(path="pic.png", alt_text="Pic", caption="My picture")
        assert img.caption == "My picture"

    def test_image_with_dimensions(self) -> None:
        img = Image(path="pic.png", alt_text="Pic", width="200px", height="100px")
        assert img.width == "200px"
        assert img.height == "100px"

    def test_image_missing_required_fields(self) -> None:
        with pytest.raises(ValidationError):
            Image(path="pic.png")


class TestParagraph:
    def test_paragraph_with_text(self) -> None:
        text = Text(content="Hello")
        para = Paragraph(children=[text])
        assert len(para.children) == 1
        assert para.children[0].content == "Hello"

    def test_paragraph_mixed_content(self) -> None:
        text = Text(content="Code: ")
        code = CodeBlock(language="py", content="x=1")
        para = Paragraph(children=[text, code])
        assert len(para.children) == 2

    def test_paragraph_empty(self) -> None:
        para = Paragraph()
        assert para.children == []


class TestSection:
    def test_section_basic(self) -> None:
        sec = Section(title="Intro", level=1)
        assert sec.title == "Intro"
        assert sec.level == 1

    def test_section_with_content(self) -> None:
        text = Text(content="Content")
        para = Paragraph(children=[text])
        sec = Section(title="Sec", level=2, children=[para])
        assert len(sec.children) == 1

    def test_section_level_validation(self) -> None:
        with pytest.raises(ValidationError):
            Section(title="Bad", level=0)

        with pytest.raises(ValidationError):
            Section(title="Bad", level=7)


class TestChapter:
    def test_chapter_basic(self) -> None:
        ch = Chapter(title="Chapter 1", number=1)
        assert ch.title == "Chapter 1"
        assert ch.number == 1

    def test_chapter_with_sections(self) -> None:
        sec = Section(title="Sec", level=1)
        ch = Chapter(title="Ch", children=[sec])
        assert len(ch.children) == 1

    def test_chapter_metadata(self) -> None:
        fm = FrontMatter(title="Meta", author="Author")
        ch = Chapter(title="Ch", metadata=fm)
        assert ch.metadata.author == "Author"


class TestBook:
    def test_book_basic(self) -> None:
        book = Book(title="My Book", author="Author Name")
        assert book.title == "My Book"
        assert book.author == "Author Name"

    def test_book_with_chapters(self) -> None:
        ch = Chapter(title="Ch1")
        book = Book(title="Book", author="Author", chapters=[ch])
        assert len(book.chapters) == 1

    def test_book_version_default(self) -> None:
        book = Book(title="Book", author="Author")
        assert book.version == "0.1.0"

    def test_book_required_fields(self) -> None:
        with pytest.raises(ValidationError):
            Book()


class TestFrontMatter:
    def test_front_matter_optional_fields(self) -> None:
        fm = FrontMatter()
        assert fm.title is None
        assert fm.author is None

    def test_front_matter_with_data(self) -> None:
        fm = FrontMatter(title="Title", author="Author", date="2026-07-13")
        assert fm.date == "2026-07-13"

    def test_front_matter_extra_fields(self) -> None:
        fm = FrontMatter(title="Title")
        fm.extra["custom"] = "value"
        assert fm.extra["custom"] == "value"
