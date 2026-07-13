"""Tests for DOCX renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig, OutputConfig, ThemeConfig
from markdown_book_builder.rendering.docx import DOCXRenderer


@pytest.fixture
def config():
    return BookConfig(
        title="Test Book",
        author="Test Author",
        source_dir="content",
        output=OutputConfig(path=Path("output/test.docx")),
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


class TestDOCXRenderer:
    def test_output_format(self):
        renderer = DOCXRenderer()
        assert renderer.output_format == "docx"

    def test_default_extension(self):
        renderer = DOCXRenderer()
        assert renderer._get_default_extension() == ".docx"

    def test_resolve_output_path_docx_extension(self, config):
        renderer = DOCXRenderer()
        output_path = renderer._resolve_output_path(config)
        assert output_path.suffix == ".docx"

    def test_format_options(self, config):
        renderer = DOCXRenderer()
        options = renderer._get_format_options(config)
        assert "--toc" in options
        assert "--toc-depth=2" in options

    def test_render_builds_docx_cmd(self, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "test.docx"
        config.output.path = output_path

        renderer = DOCXRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            cmd = mock_run.call_args[0][0]

            # Check DOCX-specific elements
            assert cmd[0] == "pandoc"
            assert "docx" in cmd
            assert "--toc" in cmd
            assert "--toc-depth=2" in cmd

    def test_is_available(self):
        with patch("shutil.which", return_value="/usr/bin/pandoc"):
            renderer = DOCXRenderer()
            assert renderer.is_available() is True
