"""Build AST from discovered Markdown files."""

from pathlib import Path

from markdown_it import MarkdownIt
from markdown_it.token import Token

from markdown_book_builder.ast_.models import Book, Chapter, Image, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.discovery.metadata import parse_front_matter

md = MarkdownIt()


def _tokens_to_ast_children(tokens: list[Token]) -> list[Text | Image]:
    """Convert markdown tokens to AST children (Text or Image nodes)."""
    children: list[Text | Image] = []
    for token in tokens:
        if token.type == "text":
            children.append(Text(content=token.content))
        elif token.type == "image":
            src = token.attrGet("src")
            path_str = str(src) if src is not None else ""
            children.append(
                Image(
                    path=path_str,
                    alt_text=token.content or "",
                )
            )
        elif token.type == "softbreak":
            children.append(Text(content="\n"))
        elif token.type == "inline" and token.children:
            children.extend(_tokens_to_ast_children(token.children))
    return children


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

    tokens = md.parse(body)
    sections: list[Section] = []
    current_section: Section | None = None
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token.type == "heading_open":
            level = int(token.tag[1])
            i += 1
            title_token = tokens[i]
            section_title = title_token.content
            current_section = Section(title=section_title, level=level)
            sections.append(current_section)
            i += 2  # skip heading_close

        elif token.type == "paragraph_open":
            i += 1
            inline_token = tokens[i]  # Should be inline token with children
            i += 1  # skip to paragraph_close
            i += 1  # skip paragraph_close

            if inline_token.type == "inline" and inline_token.children:
                ast_children = _tokens_to_ast_children(inline_token.children)
                if ast_children:
                    para = Paragraph(children=ast_children)  # type: ignore[arg-type]
                    if current_section:
                        current_section.children.append(para)
                    else:
                        temp_section = Section(title="Introduction", level=1)
                        temp_section.children.append(para)
                        sections.append(temp_section)

        else:
            i += 1

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
