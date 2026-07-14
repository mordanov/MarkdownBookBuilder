"""Tests for Pandoc PDF renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from markdown_book_builder.ast_.models import Book, Chapter, Paragraph, Section, Text
from markdown_book_builder.config.models import (
    BookConfig,
    FormattingConfig,
    HeadingStyleConfig,
    OutputConfig,
    PageLayoutConfig,
    TocConfig,
)
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


class TestPandocPreambleGeneration:
    """Tests for the LaTeX preamble sub-generators."""

    @pytest.fixture
    def renderer(self) -> PandocRenderer:
        return PandocRenderer()

    @pytest.fixture
    def default_fmt(self) -> FormattingConfig:
        return FormattingConfig()

    # --- Heading preamble ---

    def test_heading_preamble_contains_titlesec(self, renderer, default_fmt) -> None:
        result = renderer._heading_preamble(default_fmt)
        assert r"\usepackage{titlesec}" in result

    def test_heading_preamble_contains_xcolor(self, renderer, default_fmt) -> None:
        result = renderer._heading_preamble(default_fmt)
        assert r"\usepackage{xcolor}" in result

    def test_heading_preamble_h1_has_background_colorbox(self, renderer, default_fmt) -> None:
        result = renderer._heading_preamble(default_fmt)
        # Default H1 has background — should use \colorbox
        assert r"\colorbox" in result

    def test_heading_preamble_h2_no_colorbox(self, renderer, default_fmt) -> None:
        # Default H2 has no background — should NOT have a second \colorbox (one for H1 only)
        result = renderer._heading_preamble(default_fmt)
        # Split by chapter/section to isolate H2 (\section) block
        lines = result.splitlines()
        section_lines = [line for line in lines if r"\titleformat{\section}" in line]
        assert section_lines, "should have \\titleformat{\\section}"
        assert r"\colorbox" not in section_lines[0]

    def test_heading_preamble_custom_color_appears(self, renderer) -> None:
        fmt = FormattingConfig(headings={"h2": HeadingStyleConfig(font_size=18, color="#FF0000")})
        result = renderer._heading_preamble(fmt)
        assert "FF0000" in result

    def test_heading_preamble_h1_default_colors(self, renderer, default_fmt) -> None:
        result = renderer._heading_preamble(default_fmt)
        assert "1A3A5C" in result  # default H1 background
        assert "FFFFFF" in result  # default H1 text color

    # --- Page layout preamble ---

    def test_page_layout_preamble_contains_geometry(self, renderer, default_fmt) -> None:
        result = renderer._page_layout_preamble(default_fmt)
        assert r"\usepackage" in result and "geometry" in result

    def test_page_layout_preamble_a4paper(self, renderer, default_fmt) -> None:
        result = renderer._page_layout_preamble(default_fmt)
        assert "a4paper" in result

    def test_page_layout_preamble_default_margins(self, renderer, default_fmt) -> None:
        result = renderer._page_layout_preamble(default_fmt)
        assert "2.5cm" in result

    def test_page_layout_preamble_custom_margins(self, renderer) -> None:
        fmt = FormattingConfig(page=PageLayoutConfig(margin_left="3cm", margin_right="2cm"))
        result = renderer._page_layout_preamble(fmt)
        assert "left=3cm" in result
        assert "right=2cm" in result

    # --- Hyperref preamble ---

    def test_hyperref_preamble_present_when_interactive(self, renderer, default_fmt) -> None:
        result = renderer._hyperref_preamble(default_fmt)
        assert r"\usepackage[hidelinks]{hyperref}" in result

    def test_hyperref_preamble_absent_when_not_interactive(self, renderer) -> None:
        fmt = FormattingConfig(toc=TocConfig(interactive=False))
        result = renderer._hyperref_preamble(fmt)
        assert "hyperref" not in result

    def test_hyperref_after_titlesec_in_full_preamble(self, renderer, config) -> None:
        result_path = renderer._get_xelatex_preamble(config)
        content = Path(result_path).read_text()
        titlesec_pos = content.find("titlesec")
        hyperref_pos = content.find("hyperref")
        assert titlesec_pos != -1 and hyperref_pos != -1
        assert hyperref_pos > titlesec_pos
