"""Front matter parsing from Markdown files."""
from typing import Any


def parse_front_matter(content: str) -> tuple[dict[str, Any], str]:
    """Parse YAML front matter from Markdown content.

    Args:
        content: Full file content including front matter

    Returns:
        Tuple of (metadata dict, remaining content)

    Raises:
        ValueError: If front matter is invalid YAML
    """
    # TODO: T042 - Implement YAML front matter extraction
    raise NotImplementedError("Front matter parsing to be implemented in Phase 5")
