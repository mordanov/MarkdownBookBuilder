"""Tests for external plugin loading."""

from typing import Any
from unittest.mock import MagicMock, patch

from markdown_book_builder.config.models import PluginsConfig
from markdown_book_builder.plugins.external import load_external_plugins


def _make_ep(name: str, group: str, loaded_value: Any) -> MagicMock:
    """Create a mock EntryPoint that returns loaded_value when .load() is called."""
    ep = MagicMock()
    ep.name = name
    ep.group = group
    ep.load.return_value = loaded_value
    return ep


class TestLoadRendererEntryPoint:
    def test_load_entry_point_renderer(self) -> None:
        """A valid Renderer subclass entry point is registered."""
        from markdown_book_builder.rendering import Renderer

        class FakeLatexRenderer(Renderer):
            def is_available(self) -> bool:
                return True

            def render(self, files: Any, config: Any) -> Any:  # type: ignore[override]
                return files[0]

        ep = _make_ep("latex", "markdown_book_builder.renderers", FakeLatexRenderer)

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.renderers":
                return [ep]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_renderer") as mock_reg,
        ):
            count = load_external_plugins()

        assert count == 1
        mock_reg.assert_called_once_with("latex", FakeLatexRenderer)

    def test_renderer_ep_not_a_class_is_skipped(self) -> None:
        """A non-class renderer entry point is skipped without raising."""
        ep = _make_ep("bad", "markdown_book_builder.renderers", object())

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.renderers":
                return [ep]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_renderer") as mock_reg,
        ):
            count = load_external_plugins()

        assert count == 0
        mock_reg.assert_not_called()


class TestLoadDiagramRendererEntryPoint:
    def test_load_entry_point_diagram_renderer(self) -> None:
        """A valid DiagramRenderer subclass entry point is registered."""
        from markdown_book_builder.plugins.diagram import DiagramRenderer

        class FakeDotRenderer(DiagramRenderer):
            name = "dot"

            def is_available(self) -> bool:
                return True

            def render(self, code: str, fmt: str = "svg") -> str | None:
                return None

            def supports(self, diagram_type: str) -> bool:
                return diagram_type == "dot"

        ep = _make_ep("dot", "markdown_book_builder.diagram_renderers", FakeDotRenderer)

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.diagram_renderers":
                return [ep]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_diagram_renderer") as mock_reg,
        ):
            count = load_external_plugins()

        assert count == 1
        assert mock_reg.call_count == 1
        call_args = mock_reg.call_args
        assert call_args[0][0] == "dot"
        assert isinstance(call_args[0][1], FakeDotRenderer)

    def test_load_diagram_renderer_instance_entry_point(self) -> None:
        """A DiagramRenderer instance (not class) entry point is registered directly."""
        from markdown_book_builder.plugins.diagram import DiagramRenderer

        class FakeDotRenderer(DiagramRenderer):
            name = "dot2"

            def is_available(self) -> bool:
                return True

            def render(self, code: str, fmt: str = "svg") -> str | None:
                return None

            def supports(self, t: str) -> bool:
                return False

        instance = FakeDotRenderer()
        ep = _make_ep("dot2", "markdown_book_builder.diagram_renderers", instance)

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.diagram_renderers":
                return [ep]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_diagram_renderer") as mock_reg,
        ):
            load_external_plugins()

        mock_reg.assert_called_once_with("dot2", instance)


class TestLoadImageProviderEntryPoint:
    def test_load_entry_point_image_provider(self) -> None:
        """A valid ImageProvider subclass entry point is registered."""
        from markdown_book_builder.plugins.image import ImageProvider

        class FakeS3Provider(ImageProvider):
            name = "s3"

            def get_image(self, key: str) -> bytes | None:
                return None

            def put_image(self, key: str, data: bytes) -> None:
                pass

        ep = _make_ep("s3", "markdown_book_builder.image_providers", FakeS3Provider)

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.image_providers":
                return [ep]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_image_provider") as mock_reg,
        ):
            count = load_external_plugins()

        assert count == 1
        call_args = mock_reg.call_args
        assert call_args[0][0] == "s3"
        assert isinstance(call_args[0][1], FakeS3Provider)


class TestLoadValidatorEntryPoint:
    def test_load_entry_point_validator(self) -> None:
        """A valid Validator subclass entry point is registered."""
        from markdown_book_builder.ast_.models import Book
        from markdown_book_builder.config.models import BookConfig
        from markdown_book_builder.core.errors import ValidationError
        from markdown_book_builder.plugins.validator import Validator

        class FakeValidator(Validator):
            name = "fake"

            def validate(self, book: Book, config: BookConfig) -> list[ValidationError]:
                return []

        ep = _make_ep("fake", "markdown_book_builder.validators", FakeValidator)

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.validators":
                return [ep]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_validator") as mock_reg,
        ):
            count = load_external_plugins()

        assert count == 1
        assert mock_reg.call_count == 1
        assert isinstance(mock_reg.call_args[0][0], FakeValidator)


class TestInvalidEntryPointHandling:
    def test_invalid_entry_point_load_raises_import_error(self) -> None:
        """An entry point whose .load() raises ImportError is skipped; no exception."""
        ep = MagicMock()
        ep.name = "broken"
        ep.load.side_effect = ImportError("module not found")

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.renderers":
                return [ep]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_renderer") as mock_reg,
        ):
            count = load_external_plugins()

        assert count == 0
        mock_reg.assert_not_called()

    def test_invalid_entry_point_load_raises_arbitrary_exception(self) -> None:
        """An entry point whose .load() raises any exception is skipped without crash."""
        ep = MagicMock()
        ep.name = "bad_renderer"
        ep.load.side_effect = RuntimeError("something went wrong")

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.renderers":
                return [ep]
            return []

        with patch(
            "markdown_book_builder.plugins.external.entry_points",
            side_effect=ep_side_effect,
        ):
            count = load_external_plugins()

        assert count == 0


class TestDisabledPlugins:
    def test_disabled_plugins_unregistered(self) -> None:
        """Plugins in config.disabled are unregistered after loading."""
        config = PluginsConfig(disabled=["mermaid"])

        with (
            patch("markdown_book_builder.plugins.external.entry_points", return_value=[]),
            patch("markdown_book_builder.plugins.external.unregister_renderer") as mock_ur,
            patch("markdown_book_builder.plugins.external.unregister_diagram_renderer") as mock_udr,
            patch("markdown_book_builder.plugins.external.unregister_image_provider") as mock_uip,
            patch("markdown_book_builder.plugins.external.unregister_validator") as mock_uv,
        ):
            load_external_plugins(config)

        mock_ur.assert_called_once_with("mermaid")
        mock_udr.assert_called_once_with("mermaid")
        mock_uip.assert_called_once_with("mermaid")
        mock_uv.assert_called_once_with("mermaid")

    def test_disabled_not_applied_when_config_is_none(self) -> None:
        """With config=None, unregister functions are never called."""
        with (
            patch("markdown_book_builder.plugins.external.entry_points", return_value=[]),
            patch("markdown_book_builder.plugins.external.unregister_renderer") as mock_ur,
        ):
            load_external_plugins(None)

        mock_ur.assert_not_called()


class TestExtraPlugins:
    def test_extra_plugins_imported(self) -> None:
        """Modules listed in config.extra_plugins are imported."""
        config = PluginsConfig(extra_plugins=["mymodule.plugin"])

        fake_module = MagicMock()
        del fake_module.register_plugins

        with (
            patch("markdown_book_builder.plugins.external.entry_points", return_value=[]),
            patch(
                "markdown_book_builder.plugins.external.importlib.import_module",
                return_value=fake_module,
            ) as mock_import,
        ):
            count = load_external_plugins(config)

        mock_import.assert_called_once_with("mymodule.plugin")
        assert count == 1

    def test_extra_plugins_calls_register_plugins_if_present(self) -> None:
        """If imported module exposes register_plugins(registry), it is called."""
        from markdown_book_builder.plugins.registry import _registry

        config = PluginsConfig(extra_plugins=["mymodule.plugin"])
        fake_module = MagicMock()
        fake_module.register_plugins = MagicMock()

        with (
            patch("markdown_book_builder.plugins.external.entry_points", return_value=[]),
            patch(
                "markdown_book_builder.plugins.external.importlib.import_module",
                return_value=fake_module,
            ),
        ):
            load_external_plugins(config)

        fake_module.register_plugins.assert_called_once_with(_registry)

    def test_extra_plugin_import_failure_is_skipped(self) -> None:
        """A failing extra_plugins import emits a warning but does not crash."""
        config = PluginsConfig(extra_plugins=["nonexistent.pkg"])

        with (
            patch("markdown_book_builder.plugins.external.entry_points", return_value=[]),
            patch(
                "markdown_book_builder.plugins.external.importlib.import_module",
                side_effect=ModuleNotFoundError("no module named 'nonexistent'"),
            ),
        ):
            count = load_external_plugins(config)

        assert count == 0


class TestReturnCount:
    def test_returns_zero_with_no_plugins(self) -> None:
        """Returns 0 when no entry points are found and no extra_plugins."""
        with patch("markdown_book_builder.plugins.external.entry_points", return_value=[]):
            count = load_external_plugins()
        assert count == 0

    def test_returns_correct_count_for_multiple_plugins(self) -> None:
        """Returns sum of successfully loaded plugins across all groups."""
        from markdown_book_builder.rendering import Renderer

        class FakeRenderer1(Renderer):
            def is_available(self) -> bool:
                return True

            def render(self, files: Any, config: Any) -> Any:  # type: ignore[override]
                return files[0]

        class FakeRenderer2(Renderer):
            def is_available(self) -> bool:
                return True

            def render(self, files: Any, config: Any) -> Any:  # type: ignore[override]
                return files[0]

        ep1 = _make_ep("fmt1", "markdown_book_builder.renderers", FakeRenderer1)
        ep2 = _make_ep("fmt2", "markdown_book_builder.renderers", FakeRenderer2)

        def ep_side_effect(group: str) -> list[MagicMock]:
            if group == "markdown_book_builder.renderers":
                return [ep1, ep2]
            return []

        with (
            patch(
                "markdown_book_builder.plugins.external.entry_points",
                side_effect=ep_side_effect,
            ),
            patch("markdown_book_builder.plugins.external.register_renderer"),
        ):
            count = load_external_plugins()

        assert count == 2
