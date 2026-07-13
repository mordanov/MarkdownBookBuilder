"""Diagram renderer plugins."""

import shutil
import subprocess
import tempfile
from abc import ABC, abstractmethod
from pathlib import Path
from typing import ClassVar


class DiagramRenderer(ABC):
    """Base class for diagram renderers."""

    name: str

    @abstractmethod
    def is_available(self) -> bool:
        """Check if renderer is available on the system."""
        pass

    @abstractmethod
    def render(self, diagram_code: str, output_format: str = "svg") -> str | None:
        """Render diagram code to output format.

        Args:
            diagram_code: Diagram source code
            output_format: Output format (svg, png, etc.)

        Returns:
            Rendered diagram as string (SVG) or None if rendering fails
        """
        pass

    @abstractmethod
    def supports(self, diagram_type: str) -> bool:
        """Check if renderer supports given diagram type."""
        pass


class MermaidDiagramRenderer(DiagramRenderer):
    """Renderer for Mermaid diagrams."""

    name = "mermaid"

    _SUPPORTED_TYPES: ClassVar[set[str]] = {
        "classdiagram",
        "flowchart",
        "gantt",
        "graph",
        "sequencediagram",
        "statediagram",
    }

    def is_available(self) -> bool:
        return shutil.which("mmdc") is not None

    def supports(self, diagram_type: str) -> bool:
        return diagram_type.lower() in self._SUPPORTED_TYPES

    def render(self, diagram_code: str, output_format: str = "svg") -> str | None:
        """Render Mermaid diagram to SVG/PNG."""
        from markdown_book_builder.core.errors import ConfigurationError

        if not diagram_code.strip():
            return None

        if not self.is_available():
            raise ConfigurationError("mermaid-cli (mmdc) not found on PATH")

        if not self.supports(diagram_code.split()[0].lower()):
            return None

        with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
            f.write(diagram_code)
            input_file = f.name

        output_file = input_file.replace(".mmd", f".{output_format}")

        try:
            result = subprocess.run(
                ["mmdc", "-i", input_file, "-o", output_file],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )

            if result.returncode != 0:
                return None

            with open(output_file) as f:
                return f.read()

        except (FileNotFoundError, subprocess.TimeoutExpired):
            return None
        finally:
            Path(input_file).unlink(missing_ok=True)
            Path(output_file).unlink(missing_ok=True)
