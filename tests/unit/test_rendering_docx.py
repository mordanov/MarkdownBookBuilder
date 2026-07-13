"""Tests for DOCX renderer."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

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
def sample_files(tmp_path):
    files = []
    for i in range(2):
        f = tmp_path / f"chapter{i}.md"
        f.write_text(f"# Chapter {i}\n\nContent")
        files.append(f)
    return files


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

    def test_render_builds_docx_cmd(self, config, sample_files, tmp_path):
        output_path = tmp_path / "output" / "test.docx"
        config.output.path = output_path

        renderer = DOCXRenderer()
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            renderer.render(sample_files, config)

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
