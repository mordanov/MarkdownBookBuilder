"""Tests for HTML renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

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
def sample_files(tmp_path):
    files = []
    for i in range(2):
        f = tmp_path / f"chapter{i}.md"
        f.write_text(f"# Chapter {i}\n\nContent")
        files.append(f)
    return files


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

    def test_render_builds_html_cmd(self, config, sample_files, tmp_path):
        output_path = tmp_path / "output" / "test.html"
        config.output.path = output_path

        renderer = HTMLRenderer()
        with (
            patch("shutil.which", return_value="/usr/bin/pandoc"),
            patch("subprocess.run") as mock_run,
        ):
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_files, config)

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
