"""Chapter ordering from configuration or file system order."""

from pathlib import Path

import yaml  # type: ignore[import-untyped]


def load_order_config(path: Path) -> list[str]:
    """Load chapter ordering from order.yaml.

    Args:
        path: Path to order.yaml file

    Returns:
        List of filenames in desired order

    Raises:
        FileNotFoundError: If order file doesn't exist
        ValueError: If order file is invalid
    """
    try:
        content = path.read_text(encoding="utf-8")
        data = yaml.safe_load(content) or {}

        if "order" not in data:
            return []

        order = data["order"]
        if not isinstance(order, list):
            raise ValueError("'order' must be a list of filenames")

        return [str(item) for item in order]
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid YAML in order file: {e}") from e


def sort_chapters(files: list[Path], order: list[str] | None = None) -> list[Path]:
    """Sort files according to order config or alphabetically.

    Args:
        files: List of file paths
        order: Optional list of filenames in desired order

    Returns:
        Sorted list of file paths
    """
    if not order:
        return sorted(files)

    filename_to_path = {f.name: f for f in files}

    ordered = []
    for filename in order:
        if filename in filename_to_path:
            ordered.append(filename_to_path[filename])

    for f in files:
        if f not in ordered:
            ordered.append(f)

    return ordered
