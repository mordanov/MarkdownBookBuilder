"""Markdown Book Builder: Developer-focused book processing pipeline.

Convert collections of Markdown documents into professionally typeset books (PDFs)
with deterministic, reproducible builds and AI-assisted image generation.
"""

__version__ = "0.1.0"
__author__ = "Aleksandr Mordanov"
__license__ = "MIT"

from markdown_book_builder.core.errors import (
    BookBuilderError,
    ConfigurationError,
    DiscoveryError,
    ValidationError,
)

__all__ = [
    "BookBuilderError",
    "ConfigurationError",
    "DiscoveryError",
    "ValidationError",
]
