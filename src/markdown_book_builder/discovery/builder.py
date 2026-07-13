"""Build AST from discovered Markdown files."""

from pathlib import Path
from typing import Any

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.discovery.metadata import parse_front_matter


def parse_markdown_file(path: Path) -> Chapter:
    """Parse single Markdown file into Chapter AST.

    Args:
        path: Path to Markdown file

    Returns:
        Chapter AST node

    Raises:
        FileNotFoundError: If file doesn't exist
    """
    content = path.read_text(encoding="utf-8")
    metadata, body = parse_front_matter(content)

    title = metadata.get("title", path.stem)
    number = metadata.get("number", None)

    sections: list[Section] = []
    current_level = 0
    current_content: list[str] = []

    for line in body.split("\n"):
        if line.startswith("#"):
            if current_content and current_level > 0:
                text = Text(content="\n".join(current_content).strip())
                para = Paragraph(children=[text])
                section = Section(
                    title=f"Section {len(sections)}", level=current_level, children=[para]
                )
                sections.append(section)
                current_content = []

            hashes = len(line) - len(line.lstrip("#"))
            section_title = line.lstrip("#").strip()
            current_level = min(hashes, 6)

            section = Section(title=section_title, level=current_level)
            sections.append(section)
        elif line.strip() and current_level > 0:
            current_content.append(line)

    if current_content:
        text = Text(content="\n".join(current_content).strip())
        para = Paragraph(children=[text])
        if sections and sections[-1].children == []:
            sections[-1].children = [para]

    return Chapter(title=str(title), number=number, children=sections)  # type: ignore[arg-type]


def build_ast_from_files(files: list[Path], config: BookConfig) -> Book:
    """Convert Markdown files to Book AST.

    Args:
        files: List of Markdown file paths
        config: Book configuration

    Returns:
        Book AST

    Raises:
        ValueError: If files are invalid or empty
    """
    if not files:
        raise ValueError("No Markdown files found")

    chapters = []
    for path in files:
        chapter = parse_markdown_file(path)
        chapters.append(chapter)

    return Book(
        title=config.title,
        author=config.author,
        version=config.version,
        chapters=chapters,
    )
