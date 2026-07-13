"""Tests for theme resolver."""

from pathlib import Path

import pytest

from markdown_book_builder.themes.resolver import ThemeResolver, load_theme_css


class TestThemeResolver:
    def test_list_builtin_themes(self):
        resolver = ThemeResolver()
        themes = resolver.list_builtin_themes()
        assert isinstance(themes, list)
        assert "default" in themes
        assert "dark" in themes
        assert "minimal" in themes

    def test_load_builtin_theme_default(self):
        resolver = ThemeResolver()
        css = resolver.get_theme_css("default")
        assert css is not None
        assert isinstance(css, str)
        assert len(css) > 0
        assert "--primary-color" in css  # Check for CSS variable

    def test_load_builtin_theme_dark(self):
        resolver = ThemeResolver()
        css = resolver.get_theme_css("dark")
        assert css is not None
        assert isinstance(css, str)
        assert "#1a1a1a" in css  # Dark background color

    def test_load_builtin_theme_minimal(self):
        resolver = ThemeResolver()
        css = resolver.get_theme_css("minimal")
        assert css is not None
        assert isinstance(css, str)

    def test_theme_not_found(self):
        resolver = ThemeResolver()
        css = resolver.get_theme_css("nonexistent-theme")
        assert css is None

    def test_cache_builtin_theme(self):
        resolver = ThemeResolver()
        css1 = resolver.get_theme_css("default")
        css2 = resolver.get_theme_css("default")
        assert css1 == css2

    def test_load_project_theme(self, tmp_path):
        # Create a custom theme in project
        theme_dir = tmp_path / "themes"
        theme_dir.mkdir()
        custom_css = theme_dir / "custom.css"
        custom_css.write_text("body { color: purple; }")

        resolver = ThemeResolver()
        css = resolver.get_theme_css("custom", project_dir=tmp_path)
        assert css is not None
        assert "purple" in css

    def test_module_level_load_theme_css(self):
        css = load_theme_css("default")
        assert css is not None
        assert len(css) > 0

    def test_module_level_load_theme_css_not_found(self):
        css = load_theme_css("nonexistent")
        assert css is None
