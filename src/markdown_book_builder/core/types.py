"""Type aliases and constants for Markdown Book Builder."""

from pathlib import Path
from typing import TypeAlias

# Path types
FilePath: TypeAlias = Path | str
DirectoryPath: TypeAlias = Path | str

# Common constants
DEFAULT_OUTPUT_FORMAT = "pdf"
SUPPORTED_OUTPUT_FORMATS = {"pdf", "html", "epub", "docx"}
SUPPORTED_LANGUAGES = {
    "python",
    "javascript",
    "typescript",
    "java",
    "cpp",
    "c",
    "rust",
    "go",
    "bash",
    "shell",
    "yaml",
    "json",
    "toml",
    "markdown",
    "html",
    "css",
    "sql",
}

# Configuration defaults
DEFAULT_CONFIG_FILE = "book.toml"
DEFAULT_ENV_FILE = ".book.env"
DEFAULT_ENCODING = "utf-8"

# AST and rendering defaults
DEFAULT_MAX_HEADING_LEVEL = 6
DEFAULT_IMAGE_FORMATS = {"png", "jpg", "jpeg", "gif", "svg", "webp"}
