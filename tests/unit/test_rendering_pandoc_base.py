"""Tests for Pandoc base renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig, OutputConfig, ThemeConfig
from markdown_book_builder.rendering.pandoc import PandocRenderer


@pytest.fixture
def renderer():
    return PandocRenderer()


@pytest.fixture
def config():
    return BookConfig(
        title="Test Book",
        author="Test Author",
        source_dir="content",
        output=OutputConfig(path=Path("output/test.pdf")),
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


class TestPandocBaseRenderer:
    def test_is_available_true(self):
        with patch("shutil.which", return_value="/usr/bin/pandoc"):
            renderer = PandocRenderer()
            assert renderer.is_available() is True

    def test_is_available_false(self):
        with patch("shutil.which", return_value=None):
            renderer = PandocRenderer()
            assert renderer.is_available() is False

    def test_render_creates_output_directory(self, config, sample_book, tmp_path):
        output_path = tmp_path / "deep" / "nested" / "output" / "test.pdf"
        config.output.path = output_path

        renderer = PandocRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            assert output_path.parent.exists()

    def test_render_builds_pandoc_cmd(self, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "test.pdf"
        config.output.path = output_path

        renderer = PandocRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            # Verify command was called
            mock_run.assert_called_once()
            cmd = mock_run.call_args[0][0]

            # Check key elements
            assert cmd[0] == "pandoc"
            assert "markdown" in cmd
            assert "pdf" in cmd
            assert "xelatex" in cmd
            assert "--toc" in cmd
            assert f"title={config.title}" in cmd

    def test_render_includes_author_metadata(self, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "test.pdf"
        config.output.path = output_path
        config.author = "Jane Doe"

        renderer = PandocRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            cmd = mock_run.call_args[0][0]
            assert "author=Jane Doe" in cmd or "Jane Doe" in cmd

    def test_render_pandoc_failure(self, renderer, config, sample_book):
        from markdown_book_builder.core.errors import TransformationError

        renderer = PandocRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=1, stderr="pandoc error")

            with pytest.raises(TransformationError, match="pandoc failed"):
                renderer.render(sample_book, config)

    def test_render_pandoc_not_found(self, config, sample_book):
        from markdown_book_builder.core.errors import ConfigurationError

        renderer = PandocRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run", side_effect=FileNotFoundError),
        ):
            with pytest.raises(ConfigurationError, match="pandoc not found"):
                renderer.render(sample_book, config)

    def test_resolve_output_path_pdf_extension(self, config):
        renderer = PandocRenderer()
        output_path = renderer._resolve_output_path(config)
        assert output_path.suffix == ".pdf"

    def test_get_format_options_pdf_engine(self, config):
        renderer = PandocRenderer()
        options = renderer._get_format_options(config)
        assert "--pdf-engine" in options
        assert "xelatex" in options
