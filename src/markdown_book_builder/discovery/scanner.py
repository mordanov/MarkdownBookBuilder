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
        List of Markdown file paths (absolute paths)

    Raises:
        FileNotFoundError: If directory doesn't exist
    """
    dir_path = Path(path).resolve()
    if not dir_path.is_dir():
        raise FileNotFoundError(f"Directory not found: {dir_path}")

    if recursive:
        files = list(dir_path.rglob("*.md"))
    else:
        files = list(dir_path.glob("*.md"))

    if sort:
        files.sort()

    return files
