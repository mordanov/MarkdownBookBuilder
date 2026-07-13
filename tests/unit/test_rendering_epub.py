"""Tests for EPUB renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig, OutputConfig, ThemeConfig
from markdown_book_builder.rendering.epub import EPUBRenderer


@pytest.fixture
def config():
    return BookConfig(
        title="Test Book",
        author="Test Author",
        source_dir="content",
        output=OutputConfig(path=Path("output/test.epub")),
        theme=ThemeConfig(name="default"),
    )


@pytest.fixture
def sample_book():
    """Create a sample book for rendering tests."""
    return Book(
        title="Test Book",
        author="Test Author",
        chapters=[
            Chapter(
                title="Chapter 0",
                children=[
                    Section(
                        level=2,
                        title="Section 1",
                        children=[Paragraph(children=[Text(content="Content 0")])],
                    )
                ],
            ),
            Chapter(
                title="Chapter 1",
                children=[
                    Section(
                        level=2,
                        title="Section 2",
                        children=[Paragraph(children=[Text(content="Content 1")])],
                    )
                ],
            ),
        ],
    )


class TestEPUBRenderer:
    def test_output_format(self):
        renderer = EPUBRenderer()
        assert renderer.output_format == "epub3"

    def test_default_extension(self):
        renderer = EPUBRenderer()
        assert renderer._get_default_extension() == ".epub"

    def test_resolve_output_path_epub_extension(self, config):
        renderer = EPUBRenderer()
        output_path = renderer._resolve_output_path(config)
        assert output_path.suffix == ".epub"

    def test_format_options(self, config):
        renderer = EPUBRenderer()
        options = renderer._get_format_options(config)
        assert "--toc" in options
        assert "--toc-depth=2" in options

    def test_render_builds_epub_cmd(self, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "test.epub"
        config.output.path = output_path

        renderer = EPUBRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            cmd = mock_run.call_args[0][0]

            # Check EPUB-specific elements
            assert cmd[0] == "pandoc"
            assert "epub3" in cmd
            assert "--toc" in cmd
            assert "--toc-depth=2" in cmd

    def test_is_available(self):
        with patch("shutil.which", return_value="/usr/bin/pandoc"):
            renderer = EPUBRenderer()
            assert renderer.is_available() is True
