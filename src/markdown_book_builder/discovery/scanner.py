"""File scanner for recursive Markdown discovery."""

from pathlib import Path


def scan_directory(
    path: str | Path,
    recursive: bool = True,
    sort: bool = True,
) -> list[Path]:
    """Scan directory for Markdown files.

    Args:
        path: Directory to scan
        recursive: Recursively scan subdirectories
        sort: Sort files lexicographically

    Returns:
        List of Markdown file paths

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    # TODO: T041 - Implement recursive scanner with ordering
    raise NotImplementedError("Directory scanning to be implemented in Phase 5")
