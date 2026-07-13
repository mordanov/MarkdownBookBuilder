"""Tests for HTML renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig, OutputConfig, ThemeConfig
from markdown_book_builder.rendering.html import HTMLRenderer


@pytest.fixture
def config():
    return BookConfig(
        title="Test Book",
        author="Test Author",
        source_dir="content",
        output=OutputConfig(path=Path("output/test.html")),
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


class TestHTMLRenderer:
    def test_output_format(self):
        renderer = HTMLRenderer()
        assert renderer.output_format == "html5"

    def test_default_extension(self):
        renderer = HTMLRenderer()
        assert renderer._get_default_extension() == ".html"

    def test_resolve_output_path_html_extension(self, config):
        renderer = HTMLRenderer()
        output_path = renderer._resolve_output_path(config)
        assert output_path.suffix == ".html"

    def test_format_options(self, config):
        renderer = HTMLRenderer()
        options = renderer._get_format_options(config)
        assert "--standalone" in options
        assert "--self-contained" in options

    def test_render_builds_html_cmd(self, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "test.html"
        config.output.path = output_path

        renderer = HTMLRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            cmd = mock_run.call_args[0][0]

            # Check HTML-specific elements
            assert cmd[0] == "pandoc"
            assert "html5" in cmd
            assert "--standalone" in cmd
            assert "--self-contained" in cmd
            assert "--toc" in cmd

    def test_is_available(self):
        with patch("shutil.which", return_value="/usr/bin/pandoc"):
            renderer = HTMLRenderer()
            assert renderer.is_available() is True
