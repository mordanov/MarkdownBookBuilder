"""Image provider plugins."""

from abc import ABC, abstractmethod


class ImageProvider(ABC):
    """Base class for image providers."""

    name: str

    @abstractmethod
    def get_image(self, key: str) -> bytes | None:
        """Get image from provider.

        Args:
            key: Image identifier/cache key

        Returns:
            Image data as bytes, or None if not found
        """
        pass

    @abstractmethod
    def put_image(self, key: str, data: bytes) -> None:
        """Store image in provider.

        Args:
            key: Image identifier/cache key
            data: Image data as bytes
        """
        pass
