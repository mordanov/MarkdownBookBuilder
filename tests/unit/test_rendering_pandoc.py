"""Tests for Pandoc PDF renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig, OutputConfig
from markdown_book_builder.core.errors import ConfigurationError, TransformationError
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
        output=OutputConfig(path=Path("output/test.pdf"), pdf_engine="xelatex"),
    )


@pytest.fixture
def sample_book():
    """Create a sample book for rendering tests."""
    return Book(
        title="Test Book",
        author="Test Author",
        chapters=[
            Chapter(
                title=f"Chapter {i}",
                children=[
                    Section(
                        level=2,
                        title=f"Section {i}",
                        children=[Paragraph(children=[Text(content=f"Content for chapter {i}")])],
                    )
                ],
            )
            for i in range(3)
        ],
    )


class TestPandocRendererAvailability:
    def test_is_available_true(self):
        with patch("shutil.which", return_value="/usr/bin/pandoc"):
            renderer = PandocRenderer()
            assert renderer.is_available() is True

    def test_is_available_false(self):
        with patch("shutil.which", return_value=None):
            renderer = PandocRenderer()
            assert renderer.is_available() is False


class TestPandocRendererRender:
    def test_render_success(self, renderer, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "book.pdf"
        config.output.path = output_path

        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)

            result = renderer.render(sample_book, config)

            assert result == output_path
            assert output_path.parent.exists()
            mock_run.assert_called_once()

            # Verify command structure
            call_args = mock_run.call_args
            cmd = call_args[0][0]
            assert cmd[0] == "pandoc"
            assert "markdown" in cmd
            assert "pdf" in cmd
            assert "xelatex" in cmd
            assert "--toc" in cmd
            assert str(output_path) in cmd

    def test_render_pandoc_failure(self, renderer, config, sample_book):
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=1, stderr="pandoc: Unknown writer format")

            with pytest.raises(TransformationError, match="pandoc failed"):
                renderer.render(sample_book, config)

    def test_render_pandoc_not_found(self, renderer, config, sample_book):
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run", side_effect=FileNotFoundError),
        ):
            with pytest.raises(ConfigurationError, match="pandoc not found"):
                renderer.render(sample_book, config)

    def test_render_with_author(self, renderer, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "book.pdf"
        config.output.path = output_path
        config.author = "Jane Doe"

        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            call_args = mock_run.call_args
            cmd = call_args[0][0]
            assert "author=Jane Doe" in cmd or "Jane Doe" in cmd

    def test_render_creates_output_directory(self, renderer, config, sample_book, tmp_path):
        output_path = tmp_path / "deep" / "nested" / "output" / "book.pdf"
        config.output.path = output_path

        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            assert output_path.parent.exists()

    def test_render_not_available(self, renderer, config, sample_book):
        with patch.object(renderer, "is_available", return_value=False):
            with pytest.raises(ConfigurationError, match="pandoc not found"):
                renderer.render(sample_book, config)

    def test_render_custom_pdf_engine(self, renderer, config, sample_book, tmp_path):
        output_path = tmp_path / "output" / "book.pdf"
        config.output.path = output_path
        config.output.pdf_engine = "pdflatex"

        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_book, config)

            call_args = mock_run.call_args
            cmd = call_args[0][0]
            assert "pdflatex" in cmd
