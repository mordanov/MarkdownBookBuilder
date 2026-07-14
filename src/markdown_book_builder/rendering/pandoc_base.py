"""Base class for Pandoc-backed renderers."""

import subprocess
import tempfile
from abc import abstractmethod
from pathlib import Path

from markdown_book_builder.ast_.models import Book, Chapter, Image, Paragraph, Section, Text
from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.errors import ConfigurationError, TransformationError
from markdown_book_builder.core.logging import get_logger
from markdown_book_builder.rendering.base import Renderer
from markdown_book_builder.themes import load_theme_css

logger = get_logger(__name__)


class PandocBaseRenderer(Renderer):
    """Base class for renderers using Pandoc."""

    output_format: str  # Subclasses override this

    def is_available(self) -> bool:
        """Pandoc-based renderers only require pandoc on PATH."""
        import shutil

        return shutil.which("pandoc") is not None

    def render(self, book: Book, config: BookConfig) -> Path:
        """Render book AST using Pandoc."""
        if not self.is_available():
            raise ConfigurationError("pandoc not found on PATH")

        output_path = self._resolve_output_path(config)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        md_files = self._book_to_temp_markdown(book)
        cmd = self._build_pandoc_cmd(md_files, output_path, config)

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=6000, check=False)
        except FileNotFoundError as e:
            raise ConfigurationError("pandoc not found on PATH") from e

        if proc.returncode != 0:
            raise TransformationError(f"pandoc failed: {proc.stderr}")

        return output_path

    def _resolve_output_path(self, config: BookConfig) -> Path:
        """Resolve output path based on format and config."""
        output_base = config.output.path
        # If path doesn't have the right extension for this format, replace it
        if output_base.suffix not in self._get_valid_extensions():
            output_base = output_base.with_suffix(self._get_default_extension())
        return output_base

    def _get_valid_extensions(self) -> set[str]:
        """Valid file extensions for this format."""
        return {self._get_default_extension()}

    @abstractmethod
    def _get_default_extension(self) -> str:
        """Default file extension for this format (e.g., '.pdf')."""
        pass

    def _build_pandoc_cmd(
        self, files: list[Path], output_path: Path, config: BookConfig
    ) -> list[str]:
        """Build the pandoc command line."""
        cmd = [
            "pandoc",
            *[str(f) for f in files],
            "--from",
            "markdown",
            "--to",
            self.output_format,
            "--toc",
            "--metadata",
            f"title={config.title}",
        ]

        if config.author:
            cmd.extend(["--metadata", f"author={config.author}"])

        # Add theme CSS if available
        theme_css = load_theme_css(config.theme.name)
        if theme_css:
            # For HTML-based formats, pass CSS via --css
            if self.output_format in ("html", "html5"):
                # Write CSS to temp file and reference it
                import tempfile

                with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
                    f.write(theme_css)
                    css_file = f.name
                cmd.extend(["--css", css_file])
            # For EPUB, also use --css
            elif self.output_format == "epub3":
                import tempfile

                with tempfile.NamedTemporaryFile(mode="w", suffix=".css", delete=False) as f:
                    f.write(theme_css)
                    css_file = f.name
                cmd.extend(["--css", css_file])

        # Format-specific options
        cmd.extend(self._get_format_options(config))

        # Output file
        cmd.extend(["-o", str(output_path)])

        return cmd

    def _get_format_options(self, config: BookConfig) -> list[str]:
        """Additional pandoc options for this format.

        Override in subclasses for format-specific options.
        """
        return []

    def _book_to_temp_markdown(self, book: Book) -> list[Path]:
        """Convert Book AST to temporary markdown files.

        Returns list of temporary file paths with updated image references.
        """
        temp_dir = tempfile.mkdtemp(prefix="mbb_render_")
        temp_files = []

        for chapter in book.chapters:
            md_content = self._chapter_to_markdown(chapter)
            temp_file = Path(temp_dir) / f"{chapter.title.replace('/', '_')}.md"
            temp_file.write_text(md_content, encoding="utf-8")
            temp_files.append(temp_file)
            logger.debug(f"Created temp markdown: {temp_file}")

        return temp_files

    def _chapter_to_markdown(self, chapter: Chapter) -> str:
        """Convert Chapter AST to markdown string."""
        lines = [f"# {chapter.title}\n"]

        for child in chapter.children:
            if isinstance(child, Section):
                lines.append(self._section_to_markdown(child, level=1))

        return "\n".join(lines)

    def _section_to_markdown(self, section: Section, level: int) -> str:
        """Convert Section AST to markdown string."""
        lines = [f"{'#' * (level + 1)} {section.title}\n"]

        for child in section.children:
            if isinstance(child, Paragraph):
                para_text = "".join(
                    self._node_to_markdown(n)
                    for n in child.children
                    if isinstance(n, (Text, Image))
                )
                lines.append(para_text)
                lines.append("")
            elif isinstance(child, Section):
                lines.append(self._section_to_markdown(child, level + 1))

        return "\n".join(lines)

    def _node_to_markdown(self, node: Text | Image) -> str:
        """Convert AST node to markdown."""
        if isinstance(node, Text):
            return node.content
        elif isinstance(node, Image):
            if node.path:
                return f"![{node.alt_text}]({node.path})"
            else:
                return f"*{node.alt_text}*"
        return ""
