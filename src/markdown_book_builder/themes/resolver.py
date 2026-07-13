"""Theme resolution and loading."""

from pathlib import Path

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)

# Built-in themes directory
BUILTIN_THEMES_DIR = Path(__file__).parent / "builtin"


class ThemeResolver:
    """Resolves and loads theme CSS files."""

    def __init__(self) -> None:
        self._cache: dict[str, str] = {}

    def get_theme_css(self, theme_name: str, project_dir: Path | None = None) -> str | None:
        """Load theme CSS content.

        Args:
            theme_name: Theme name (e.g., 'dark') or path to CSS file
            project_dir: Project directory to search for custom themes

        Returns:
            CSS content as string, or None if theme not found
        """
        # Check cache first
        if theme_name in self._cache:
            return self._cache[theme_name]

        css_content = None

        # Try as built-in theme
        builtin_path = BUILTIN_THEMES_DIR / f"{theme_name}.css"
        if builtin_path.exists():
            css_content = builtin_path.read_text()
            logger.debug(f"Loaded built-in theme: {theme_name}")
        # Try as project-relative path
        elif project_dir:
            project_path = project_dir / "themes" / f"{theme_name}.css"
            if project_path.exists():
                css_content = project_path.read_text()
                logger.debug(f"Loaded project theme: {theme_name}")
        # Try as absolute path
        elif Path(theme_name).exists():
            try:
                css_content = Path(theme_name).read_text()
                logger.debug(f"Loaded custom theme: {theme_name}")
            except Exception as e:
                logger.warning(f"Failed to load custom theme {theme_name}: {e}")

        if css_content:
            self._cache[theme_name] = css_content

        return css_content

    def list_builtin_themes(self) -> list[str]:
        """List available built-in themes."""
        if not BUILTIN_THEMES_DIR.exists():
            return []
        return sorted([f.stem for f in BUILTIN_THEMES_DIR.glob("*.css")])


# Global singleton
_resolver = ThemeResolver()


def load_theme_css(
    theme_name: str,
    project_dir: Path | None = None,
) -> str | None:
    """Load theme CSS content.

    Args:
        theme_name: Theme name (e.g., 'dark') or path to CSS file
        project_dir: Project directory to search for custom themes

    Returns:
        CSS content as string, or None if theme not found
    """
    return _resolver.get_theme_css(theme_name, project_dir)
