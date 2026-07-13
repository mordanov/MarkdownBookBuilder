"""Front matter parsing from Markdown files."""

from datetime import date
from pathlib import Path
from typing import Any

import yaml

from markdown_book_builder.ast_.models import FrontMatter


def parse_front_matter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML front matter from Markdown content.

    Args:
        content: Full file content including front matter

    Returns:
        Tuple of (metadata dict, remaining content)

    Raises:
        ValueError: If front matter is invalid YAML
    """
    if not content.startswith("---"):
        return {}, content

    lines = content.split("\n")
    end_idx = None

    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, content

    fm_content = "\n".join(lines[1:end_idx])
    remaining = "\n".join(lines[end_idx + 1 :])

    try:
        data = yaml.safe_load(fm_content) or {}
        for key, value in data.items():
            if isinstance(value, date):
                data[key] = value.isoformat()
        return data, remaining.lstrip("\n")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML front matter: {e}") from e


def extract_front_matter(path: Path) -> FrontMatter:
    """Extract front matter from a Markdown file.

    Args:
        path: Path to Markdown file

    Returns:
        FrontMatter object

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If front matter is invalid
    """
    content = path.read_text(encoding="utf-8")
    data, _ = parse_front_matter(content)
    return FrontMatter(**data) if data else FrontMatter()
