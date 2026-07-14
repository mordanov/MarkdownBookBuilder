"""Unit tests for FormattingConfig models."""

import pytest
from pydantic import ValidationError

from markdown_book_builder.config.models import (
    _DEFAULT_HEADING_STYLES,
    FormattingConfig,
    HeadingStyleConfig,
    PageLayoutConfig,
    TocConfig,
    get_effective_headings,
)


class TestHeadingStyleConfig:
    def test_valid_hex_with_hash(self) -> None:
        s = HeadingStyleConfig(color="#1A3A5C")
        assert s.color == "1A3A5C"

    def test_valid_hex_without_hash(self) -> None:
        s = HeadingStyleConfig(color="1a3a5c")
        assert s.color == "1A3A5C"

    def test_valid_3digit_hex(self) -> None:
        s = HeadingStyleConfig(color="#FFF")
        assert s.color == "FFF"

    def test_uppercase_normalization(self) -> None:
        s = HeadingStyleConfig(color="#abcdef")
        assert s.color == "ABCDEF"

    def test_invalid_hex_raises(self) -> None:
        with pytest.raises(ValidationError):
            HeadingStyleConfig(color="#ZZZZZZ")

    def test_invalid_hex_too_short(self) -> None:
        with pytest.raises(ValidationError):
            HeadingStyleConfig(color="#12")

    def test_font_size_min_bound(self) -> None:
        s = HeadingStyleConfig(font_size=6)
        assert s.font_size == 6

    def test_font_size_max_bound(self) -> None:
        s = HeadingStyleConfig(font_size=144)
        assert s.font_size == 144

    def test_font_size_out_of_range_low(self) -> None:
        with pytest.raises(ValidationError):
            HeadingStyleConfig(font_size=5)

    def test_font_size_out_of_range_high(self) -> None:
        with pytest.raises(ValidationError):
            HeadingStyleConfig(font_size=145)

    def test_background_none_allowed(self) -> None:
        s = HeadingStyleConfig(color="#000000", background=None)
        assert s.background is None

    def test_background_valid_hex(self) -> None:
        s = HeadingStyleConfig(color="#FFFFFF", background="#1A3A5C")
        assert s.background == "1A3A5C"

    def test_background_invalid_hex_raises(self) -> None:
        with pytest.raises(ValidationError):
            HeadingStyleConfig(color="#000000", background="#GGGGGG")

    def test_defaults(self) -> None:
        s = HeadingStyleConfig()
        assert s.bold is True
        assert s.italic is False


class TestGetEffectiveHeadings:
    def test_empty_config_returns_all_defaults(self) -> None:
        result = get_effective_headings({})
        assert set(result.keys()) == {"h1", "h2", "h3", "h4", "h5", "h6"}
        assert result["h1"].font_size == _DEFAULT_HEADING_STYLES["h1"].font_size

    def test_user_override_merges_over_default(self) -> None:
        custom = HeadingStyleConfig(font_size=28, bold=True, color="#FF0000")
        result = get_effective_headings({"h1": custom})
        assert result["h1"].font_size == 28
        assert result["h1"].color == "FF0000"
        # h2 remains at default
        assert result["h2"].font_size == _DEFAULT_HEADING_STYLES["h2"].font_size

    def test_all_six_levels_present(self) -> None:
        result = get_effective_headings({})
        assert len(result) == 6


class TestPageLayoutConfig:
    def test_valid_margin_cm(self) -> None:
        p = PageLayoutConfig(margin_top="2.5cm")
        assert p.margin_top == "2.5cm"

    def test_valid_margin_in(self) -> None:
        p = PageLayoutConfig(margin_left="1in")
        assert p.margin_left == "1in"

    def test_valid_margin_mm(self) -> None:
        p = PageLayoutConfig(margin_bottom="20mm")
        assert p.margin_bottom == "20mm"

    def test_invalid_margin_format(self) -> None:
        with pytest.raises(ValidationError):
            PageLayoutConfig(margin_top="2.5 cm")

    def test_invalid_margin_no_unit(self) -> None:
        with pytest.raises(ValidationError):
            PageLayoutConfig(margin_top="25")

    def test_zero_margin_raises(self) -> None:
        with pytest.raises(ValidationError):
            PageLayoutConfig(margin_top="0cm")

    def test_defaults(self) -> None:
        p = PageLayoutConfig()
        assert p.paper_size == "a4"
        assert p.margin_top == "2.5cm"


class TestTocConfig:
    def test_defaults(self) -> None:
        t = TocConfig()
        assert t.enabled is True
        assert t.depth == 3
        assert t.interactive is True

    def test_depth_min(self) -> None:
        t = TocConfig(depth=1)
        assert t.depth == 1

    def test_depth_max(self) -> None:
        t = TocConfig(depth=6)
        assert t.depth == 6

    def test_depth_out_of_range_low(self) -> None:
        with pytest.raises(ValidationError):
            TocConfig(depth=0)

    def test_depth_out_of_range_high(self) -> None:
        with pytest.raises(ValidationError):
            TocConfig(depth=7)


class TestFormattingConfig:
    def test_empty_config_has_defaults(self) -> None:
        f = FormattingConfig()
        assert f.page.paper_size == "a4"
        assert f.toc.interactive is True
        assert f.headings == {}

    def test_headings_from_dict(self) -> None:
        f = FormattingConfig(
            headings={"h1": {"font_size": 24, "color": "#FFFFFF", "background": "#000000"}}
        )
        assert f.headings["h1"].font_size == 24
