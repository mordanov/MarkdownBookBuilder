"""Image cache index: simple JSON-based key-value store."""

import json
from pathlib import Path

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


class ImageIndex:
    """Manages image cache index as JSON file."""

    def __init__(self, cache_dir: Path) -> None:
        """Initialize index.

        Args:
            cache_dir: Directory containing cached images
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.index_file = self.cache_dir / "index.json"
        self.index = self._load_index()
        logger.info(f"📑 Image index initialized at: {self.index_file}")

    def _load_index(self) -> dict[str, str]:
        """Load index from JSON file.

        Returns:
            Dictionary mapping prompt hash to image filename
        """
        if not self.index_file.exists():
            logger.debug("Image index file not found, creating new")
            return {}

        try:
            content = self.index_file.read_text(encoding="utf-8")
            index_data = json.loads(content)
            if isinstance(index_data, dict):
                logger.info(f"📑 Loaded image index with {len(index_data)} entries")
                return index_data
            return {}
        except (json.JSONDecodeError, OSError) as e:
            logger.warning(f"Failed to load index: {e}, starting fresh")
            return {}

    def _save_index(self) -> None:
        """Save index to JSON file."""
        try:
            content = json.dumps(self.index, indent=2, ensure_ascii=False)
            self.index_file.write_text(content, encoding="utf-8")
            logger.debug(f"💾 Saved image index with {len(self.index)} entries")
        except OSError as e:
            logger.error(f"Failed to save index: {e}")

    def get(self, prompt_hash: str) -> Path | None:
        """Get cached image path by prompt hash.

        Args:
            prompt_hash: SHA256 hash of prompt

        Returns:
            Path to cached image or None if not found
        """
        if prompt_hash in self.index:
            image_filename = self.index[prompt_hash]
            image_path = self.cache_dir / image_filename
            if image_path.exists():
                logger.debug(f"✓ Found cached image: {image_path}")
                return image_path
            else:
                logger.warning(f"Index references missing file: {image_path}")
                del self.index[prompt_hash]
                self._save_index()
                return None
        return None

    def set(self, prompt_hash: str, image_path: Path) -> None:
        """Store image in index.

        Args:
            prompt_hash: SHA256 hash of prompt
            image_path: Path to image file
        """
        if not image_path.exists():
            logger.error(f"Cannot index non-existent file: {image_path}")
            return

        filename = image_path.name
        self.index[prompt_hash] = filename
        self._save_index()
        logger.info(f"📑 Indexed image: {prompt_hash} → {filename}")

    def list_all(self) -> dict[str, str]:
        """List all cached images.

        Returns:
            Dictionary of all cached images
        """
        return dict(self.index)

    def clear(self) -> int:
        """Clear all cached images.

        Returns:
            Number of files deleted
        """
        count = 0
        for filename in self.index.values():
            try:
                image_path = self.cache_dir / filename
                if image_path.exists():
                    image_path.unlink()
                    count += 1
            except OSError as e:
                logger.warning(f"Failed to delete {filename}: {e}")

        self.index.clear()
        self._save_index()
        logger.info(f"🗑️  Cleared cache: {count} images deleted")
        return count
