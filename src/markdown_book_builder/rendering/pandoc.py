import shutil
import subprocess
from pathlib import Path

from markdown_book_builder.config.models import BookConfig
from markdown_book_builder.core.errors import ConfigurationError, TransformationError
from markdown_book_builder.rendering.base import Renderer


class PandocRenderer(Renderer):
    def is_available(self) -> bool:
        return shutil.which("pandoc") is not None

    def render(self, files: list[Path], config: BookConfig) -> Path:
        if not self.is_available():
            raise ConfigurationError("pandoc not found on PATH")

        output_path = config.output.path
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cmd = [
            "pandoc",
            *[str(f) for f in files],
            "--from",
            "markdown",
            "--to",
            "pdf",
            "--pdf-engine",
            config.output.pdf_engine,
            "--toc",
            "--metadata",
            f"title={config.title}",
        ]
        if config.author:
            cmd.extend(["--metadata", f"author={config.author}"])

        cmd.extend(["-o", str(output_path)])

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=120, check=False)
        except FileNotFoundError as e:
            raise ConfigurationError("pandoc not found on PATH") from e

        if proc.returncode != 0:
            raise TransformationError(f"pandoc failed: {proc.stderr}")

        return output_path
