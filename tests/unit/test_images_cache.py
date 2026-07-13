"""Tests for image caching system."""

from pathlib import Path

import pytest

from markdown_book_builder.images.cache import (
    ImageCache,
    cache_image,
    clear_cache,
    get_cache,
    get_cached_image,
)


@pytest.fixture
def cache_dir(tmp_path: Path) -> Path:
    """Create temporary cache directory."""
    cache = tmp_path / ".cache" / "images"
    return cache


def test_cache_init(cache_dir: Path) -> None:
    """Test cache initialization."""
    cache = ImageCache(cache_dir)
    assert cache.cache_dir == cache_dir
    assert cache_dir.exists()


def test_cache_get_hash() -> None:
    """Test hash generation."""
    cache = ImageCache()
    hash1 = cache.get_hash("test prompt")
    hash2 = cache.get_hash("test prompt")

    assert hash1 == hash2
    assert len(hash1) == 64


def test_cache_store_and_retrieve(cache_dir: Path) -> None:
    """Test storing and retrieving cached image."""
    cache = ImageCache(cache_dir)
    image_data = b"fake image data"
    key = "test prompt"

    path = cache.cache_image(key, image_data)
    assert path.exists()

    retrieved = cache.get_cached_image(key)
    assert retrieved is not None
    assert retrieved.read_bytes() == image_data


def test_cache_not_found(cache_dir: Path) -> None:
    """Test cache miss."""
    cache = ImageCache(cache_dir)
    result = cache.get_cached_image("nonexistent")
    assert result is None


def test_cache_exists(cache_dir: Path) -> None:
    """Test cache existence check."""
    cache = ImageCache(cache_dir)
    key = "test"

    assert not cache.cache_exists(key)

    cache.cache_image(key, b"data")
    assert cache.cache_exists(key)


def test_cache_clear(cache_dir: Path) -> None:
    """Test clearing cache."""
    cache = ImageCache(cache_dir)

    cache.cache_image("key1", b"data1")
    cache.cache_image("key2", b"data2")
    assert len(list(cache_dir.glob("*.png"))) == 2

    count = cache.clear_cache()
    assert count == 2
    assert len(list(cache_dir.glob("*.png"))) == 0


def test_cache_clear_empty(cache_dir: Path) -> None:
    """Test clearing empty cache."""
    cache = ImageCache(cache_dir)
    count = cache.clear_cache()
    assert count == 0


def test_global_cache() -> None:
    """Test global cache instance."""
    cache1 = get_cache()
    cache2 = get_cache()
    assert cache1 is cache2


def test_global_cache_functions(tmp_path: Path) -> None:
    """Test global cache functions."""
    test_cache = ImageCache(tmp_path / "test_cache")
    import markdown_book_builder.images.cache as cache_module

    cache_module._cache = test_cache

    key = "test_key"
    data = b"test data"

    path = cache_image(key, data)
    assert path.exists()

    retrieved = get_cached_image(key)
    assert retrieved is not None

    count = clear_cache()
    assert count == 1
