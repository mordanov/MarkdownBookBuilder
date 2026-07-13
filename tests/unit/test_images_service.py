"""Tests for image processing service."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.ast_.models import Book, Chapter, Image, Paragraph, Section
from markdown_book_builder.config.models import BookConfig, OpenAIConfig
from markdown_book_builder.images.service import process_images


@pytest.fixture()
def book_with_images() -> Book:
    """Create a book with image placeholders."""
    return Book(
        title="Test Book",
        author="Test Author",
        chapters=[
            Chapter(
                title="Chapter 1",
                children=[
                    Section(
                        level=2,
                        title="Section 1",
                        children=[
                            Paragraph(children=[]),
                            Image(
                                path="placeholder1.png", alt_text="diagram 1", caption="A diagram"
                            ),
                            Paragraph(children=[]),
                            Image(path="placeholder2.png", alt_text="diagram 2", caption="Another"),
                        ],
                    )
                ],
            )
        ],
    )


@pytest.fixture()
def config() -> BookConfig:
    """Create test config with OpenAI."""
    return BookConfig(
        title="Test",
        author="Author",
        openai=OpenAIConfig(api_key="sk-test", model="gpt-4o", image_model="dall-e-3"),
    )


class TestProcessImages:
    def test_process_images_no_api_key(self, book_with_images: Book) -> None:
        """With no API key, images are skipped."""
        config = BookConfig(
            title="Test",
            author="Author",
            openai=OpenAIConfig(api_key=""),
        )

        with patch("markdown_book_builder.images.service.get_logger"):
            result = process_images(book_with_images, config)

        assert result is book_with_images
        for chapter in result.chapters:
            for node in chapter.children:
                if isinstance(node, Section):
                    for child in node.children:
                        if isinstance(child, Image):
                            assert child.path in ("placeholder1.png", "placeholder2.png")

    def test_process_images_uses_cache(self, book_with_images: Book, config: BookConfig) -> None:
        """Images found in cache are used without generation."""
        cached_path = Path("/cache/abc123.png")
        test_image_node = book_with_images.chapters[0].children[0].children[1]

        with (
            patch("markdown_book_builder.images.service.detect_placeholders") as mock_detect,
            patch("markdown_book_builder.images.service.get_cached_image") as mock_cached,
            patch("markdown_book_builder.images.service.generate_placeholder_image") as mock_gen,
            patch("markdown_book_builder.images.service.get_logger"),
        ):
            mock_placeholder = MagicMock()
            mock_placeholder.alt_text = "diagram 1"
            mock_placeholder.node = test_image_node
            mock_detect.return_value = [mock_placeholder]

            mock_cached.return_value = cached_path

            process_images(book_with_images, config)

            mock_gen.assert_not_called()
            assert mock_placeholder.node.path == str(cached_path)

    def test_process_images_generates_new(self, book_with_images: Book, config: BookConfig) -> None:
        """New images are generated and cached."""
        cached_path = Path("/cache/def456.png")
        test_image_data = b"\x89PNG\r\n\x1a\n"

        with (
            patch("markdown_book_builder.images.service.detect_placeholders") as mock_detect,
            patch("markdown_book_builder.images.service.get_cache") as mock_get_cache,
            patch("markdown_book_builder.images.service.get_cached_image") as mock_cached,
            patch("markdown_book_builder.images.service.generate_placeholder_image") as mock_gen,
            patch("markdown_book_builder.images.service.get_logger"),
        ):
            mock_placeholder = MagicMock()
            mock_placeholder.alt_text = "new diagram"
            mock_placeholder.node = Image(path="new.png", alt_text="new diagram", caption="New")
            mock_detect.return_value = [mock_placeholder]

            mock_cache = MagicMock()
            mock_get_cache.return_value = mock_cache

            mock_cached.side_effect = [None, cached_path]
            mock_gen.return_value = test_image_data

            process_images(book_with_images, config)

            mock_gen.assert_called_once_with("new diagram", config.openai)
            mock_cache.cache_image.assert_called_once_with("new diagram", test_image_data)
            assert mock_placeholder.node.path == str(cached_path)

    def test_process_images_handles_generation_failure(
        self, book_with_images: Book, config: BookConfig
    ) -> None:
        """Generation failures are handled gracefully."""
        with (
            patch("markdown_book_builder.images.service.detect_placeholders") as mock_detect,
            patch("markdown_book_builder.images.service.get_cached_image") as mock_cached,
            patch("markdown_book_builder.images.service.generate_placeholder_image") as mock_gen,
            patch("markdown_book_builder.images.service.get_logger"),
        ):
            mock_placeholder = MagicMock()
            mock_placeholder.alt_text = "bad diagram"
            mock_placeholder.node = Image(path="bad.png", alt_text="bad", caption="Bad")
            mock_detect.return_value = [mock_placeholder]

            mock_cached.return_value = None
            mock_gen.side_effect = Exception("API error")

            result = process_images(book_with_images, config)

            assert result is book_with_images

    def test_process_images_updates_all_placeholders(
        self, book_with_images: Book, config: BookConfig
    ) -> None:
        """All placeholders are processed."""
        cached_path1 = Path("/cache/1.png")
        cached_path2 = Path("/cache/2.png")
        test_section = book_with_images.chapters[0].children[0]

        with (
            patch("markdown_book_builder.images.service.detect_placeholders") as mock_detect,
            patch("markdown_book_builder.images.service.get_cached_image") as mock_cached,
            patch("markdown_book_builder.images.service.get_logger"),
        ):
            ph1 = MagicMock()
            ph1.alt_text = "diagram 1"
            ph1.node = test_section.children[1]

            ph2 = MagicMock()
            ph2.alt_text = "diagram 2"
            ph2.node = test_section.children[3]

            mock_detect.return_value = [ph1, ph2]
            mock_cached.side_effect = [cached_path1, cached_path2]

            process_images(book_with_images, config)

            assert ph1.node.path == str(cached_path1)
            assert ph2.node.path == str(cached_path2)
