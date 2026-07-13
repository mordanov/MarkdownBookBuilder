"""Pydantic models for AST node types.

Defines the core abstract syntax tree using Pydantic with validation.
All book content is represented as an AST that plugins and transformations operate on.
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class FrontMatter(BaseModel):
    """YAML front matter metadata."""

    model_config = ConfigDict(extra="allow")

    title: str | None = Field(default=None, description="Title")
    author: str | None = Field(default=None, description="Author")
    date: str | None = Field(default=None, description="Date in ISO format")
    extra: dict[str, Any] = Field(default_factory=dict, description="Additional metadata")


class Text(BaseModel):
    """Plain text content."""

    content: str = Field(..., description="Text content")


class CodeBlock(BaseModel):
    """Code block with optional syntax highlighting."""

    language: str | None = Field(default=None, description="Programming language")
    content: str = Field(..., description="Code content")
    line_numbers: bool = Field(default=False, description="Show line numbers")


class Image(BaseModel):
    """Image reference with metadata."""

    path: str = Field(..., description="Relative path to image")
    alt_text: str = Field(..., description="Alt text for accessibility")
    caption: str | None = Field(default=None, description="Image caption")
    width: str | None = Field(default=None, description="Width with units")
    height: str | None = Field(default=None, description="Height with units")


class Paragraph(BaseModel):
    """Paragraph containing mixed content."""

    children: list[Text | CodeBlock | Image] = Field(
        default_factory=list,
        description="Paragraph content",
    )


class Section(BaseModel):
    """Section with hierarchical structure."""

    title: str = Field(..., description="Section title")
    level: int = Field(..., ge=1, le=6, description="Heading level (1-6)")
    children: list["Section | Paragraph | CodeBlock | Image"] = Field(
        default_factory=list,
        description="Section content",
    )


class Chapter(BaseModel):
    """Chapter containing sections."""

    title: str = Field(..., description="Chapter title")
    number: int | None = Field(default=None, description="Chapter number")
    metadata: FrontMatter = Field(default_factory=FrontMatter, description="Metadata")
    children: list[Section | Paragraph | CodeBlock | Image] = Field(
        default_factory=list,
        description="Chapter content",
    )


class Book(BaseModel):
    """Top-level book entity."""

    title: str = Field(..., description="Book title")
    author: str | None = Field(default=None, description="Book author")
    version: str | None = Field(default="0.1.0", description="Book version")
    metadata: FrontMatter = Field(default_factory=FrontMatter, description="Metadata")
    chapters: list[Chapter] = Field(default_factory=list, description="Chapters")

    def model_post_init(self, __context: Any) -> None:
        """Allow forward references after model creation."""
        Section.model_rebuild()


# Enable forward references for recursive models
Section.model_rebuild()
Chapter.model_rebuild()
Book.model_rebuild()
