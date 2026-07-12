"""Sample AST instances for testing."""

import pytest

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

SAMPLE_FRONT_MATTER = FrontMatter(
    title="Sample Document",
    author="Test Author",
)

SAMPLE_TEXT = Text(content="Hello world")

SAMPLE_CODE_BLOCK = CodeBlock(
    language="python",
    content='print("hello")',
)

SAMPLE_IMAGE = Image(
    path="example.png",
    alt_text="Example image",
    caption="This is an example",
)

SAMPLE_PARAGRAPH = Paragraph(
    children=[SAMPLE_TEXT],
)

SAMPLE_SECTION = Section(
    title="Sample Section",
    level=2,
    children=[SAMPLE_PARAGRAPH],
)

SAMPLE_CHAPTER = Chapter(
    title="Sample Chapter",
    number=1,
    children=[SAMPLE_SECTION],
)

SAMPLE_BOOK = Book(
    title="Sample Book",
    author="Test Author",
    chapters=[SAMPLE_CHAPTER],
)


@pytest.fixture
def sample_front_matter():
    """Sample front matter for testing."""
    return SAMPLE_FRONT_MATTER


@pytest.fixture
def sample_text():
    """Sample text node for testing."""
    return SAMPLE_TEXT


@pytest.fixture
def sample_code_block():
    """Sample code block for testing."""
    return SAMPLE_CODE_BLOCK


@pytest.fixture
def sample_image():
    """Sample image node for testing."""
    return SAMPLE_IMAGE


@pytest.fixture
def sample_paragraph():
    """Sample paragraph for testing."""
    return SAMPLE_PARAGRAPH


@pytest.fixture
def sample_section():
    """Sample section for testing."""
    return SAMPLE_SECTION


@pytest.fixture
def sample_chapter():
    """Sample chapter for testing."""
    return SAMPLE_CHAPTER


@pytest.fixture
def sample_book():
    """Sample book for testing."""
    return SAMPLE_BOOK
