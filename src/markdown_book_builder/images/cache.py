"""Image caching system with hash-based keys."""

import hashlib
from pathlib import Path

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)


class ImageCache:
    """File-based image cache with hash keys."""

    def __init__(self, cache_dir: Path | None = None) -> None:
        """Initialize cache.

        Args:
            cache_dir: Directory to store cached images (default: .cache/images/)
        """
        self.cache_dir = cache_dir or Path(".cache/images")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"💾 Image cache initialized at: {self.cache_dir.absolute()}")

    def get_hash(self, key: str) -> str:
        """Generate hash for cache key.

        Args:
            key: Cache key (usually a prompt or filename)

        Returns:
            SHA256 hash of the key
        """
        return hashlib.sha256(key.encode()).hexdigest()

    def get_cached_image(self, key: str) -> Path | None:
        """Retrieve cached image path.

        Args:
            key: Cache key

        Returns:
            Path to cached image, or None if not found
        """
        hash_key = self.get_hash(key)
        image_path = self.cache_dir / f"{hash_key}.png"

        if image_path.exists():
            logger.info(f"✓ Found cached image: {image_path}")
            return image_path

        logger.debug(f"✗ No cached image for key: {hash_key}")
        return None

    def cache_image(self, key: str, image_data: bytes) -> Path:
        """Cache image data.

        Args:
            key: Cache key
            image_data: Image binary data

        Returns:
            Path to cached image
        """
        hash_key = self.get_hash(key)
        image_path = self.cache_dir / f"{hash_key}.png"
        image_path.write_bytes(image_data)
        logger.info(f"💾 Cached image to: {image_path} ({len(image_data)} bytes)")
        return image_path

    def clear_cache(self) -> int:
        """Clear all cached images.

        Returns:
            Number of files deleted
        """
        if not self.cache_dir.exists():
            return 0

        count = 0
        for file in self.cache_dir.glob("*.png"):
            file.unlink()
            count += 1

        return count

    def cache_exists(self, key: str) -> bool:
        """Check if key is cached.

        Args:
            key: Cache key

        Returns:
            True if image is cached
        """
        return self.get_cached_image(key) is not None


# Global cache instance
_cache: ImageCache | None = None


def get_cache(cache_dir: Path | None = None) -> ImageCache:
    """Get or create global cache instance.

    Args:
        cache_dir: Optional directory override

    Returns:
        ImageCache instance
    """
    global _cache
    if _cache is None:
        _cache = ImageCache(cache_dir)
    return _cache


def get_cached_image(key: str) -> Path | None:
    """Get cached image path.

    Args:
        key: Cache key

    Returns:
        Path to cached image, or None
    """
    return get_cache().get_cached_image(key)


def cache_image(key: str, image_data: bytes) -> Path:
    """Cache image data.

    Args:
        key: Cache key
        image_data: Image binary data

    Returns:
        Path to cached image
    """
    return get_cache().cache_image(key, image_data)


def clear_cache() -> int:
    """Clear all cached images.

    Returns:
        Number of files deleted
    """
    return get_cache().clear_cache()
