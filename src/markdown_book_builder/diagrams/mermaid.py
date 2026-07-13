"""Mermaid diagram rendering support."""

from markdown_book_builder.core.errors import ConfigurationError


def render_mermaid(diagram_code: str, output_format: str = "svg") -> str | None:
    """Render Mermaid diagram to SVG or PNG.

    Args:
        diagram_code: Mermaid diagram source code
        output_format: Output format ('svg' or 'png')

    Returns:
        Rendered diagram as string (SVG) or None if rendering fails

    Raises:
        ConfigurationError: If mermaid-cli is not installed
    """
    import subprocess
    import tempfile
    from pathlib import Path

    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            suffix=".mmd",
            delete=False,
        ) as f:
            f.write(diagram_code)
            input_file = f.name

        try:
            output_file = Path(input_file).with_suffix(f".{output_format}")

            result = subprocess.run(
                ["mmdc", "-i", input_file, "-o", str(output_file)],
                capture_output=True,
                timeout=30,
                check=False,
            )

            if result.returncode != 0:
                raise ConfigurationError(
                    f"Mermaid rendering failed: {result.stderr.decode()}"
                )

            if output_file.exists():
                content = output_file.read_text()
                output_file.unlink()
                return content
            else:
                return None

        finally:
            Path(input_file).unlink()

    except FileNotFoundError:
        raise ConfigurationError(
            "mermaid-cli not found. Install with: npm install -g @mermaid-js/mermaid-cli"
        ) from None
    except subprocess.TimeoutExpired:
        raise ConfigurationError("Mermaid rendering timed out") from None
    except Exception as e:
        raise ConfigurationError(f"Mermaid rendering error: {e}") from e


def validate_mermaid(diagram_code: str) -> bool:
    """Validate Mermaid diagram syntax.

    Args:
        diagram_code: Mermaid source code

    Returns:
        True if valid, False otherwise
    """
    if not diagram_code or not diagram_code.strip():
        return False

    valid_types = [
        "graph",
        "flowchart",
        "sequencediagram",
        "classdiagram",
        "statediagram",
        "gantt",
    ]

    first_line = diagram_code.strip().split("\n")[0].lower()

    return any(vtype in first_line for vtype in valid_types)
