"""Document discovery module for scanning and parsing Markdown files."""

from markdown_book_builder.discovery.builder import build_ast_from_files
from markdown_book_builder.discovery.scanner import scan_directory

__all__ = ["build_ast_from_files", "scan_directory"]
