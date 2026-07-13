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

# Load built-in plugins at import time
from markdown_book_builder.plugins.loader import load_builtin_plugins

load_builtin_plugins()

__all__ = [
    "BookBuilderError",
    "ConfigurationError",
    "DiscoveryError",
    "ValidationError",
]
