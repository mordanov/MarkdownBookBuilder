"""Main CLI application and root commands."""
import typer

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)

# Create the main Typer app
app = typer.Typer(
    help="Markdown Book Builder: Convert Markdown collections into professional books (PDF)",
    no_args_is_help=True,
)


@app.callback()
def main_callback(
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Enable verbose output (DEBUG level logging)",
    ),
) -> None:
    """Main entry point for Markdown Book Builder CLI."""
    if verbose:
        import logging
        from markdown_book_builder.core.logging import setup_logging
        setup_logging(level=logging.DEBUG)


@app.command()
def build(
    path: str = typer.Argument(
        ...,
        help="Path to Markdown directory or book.toml config file",
    ),
) -> None:
    """Build a book from Markdown files.

    Discovers Markdown files, builds AST, and renders to output format.
    """
    logger.info(f"Building book from: {path}")
    # TODO: Implementation in US4 (CLI Command Structure)
    typer.echo("Build command placeholder - implementation coming in Phase 3")


@app.command()
def validate(
    path: str = typer.Argument(
        ...,
        help="Path to Markdown directory to validate",
    ),
) -> None:
    """Validate book structure and Markdown content.

    Checks for errors, missing files, and configuration issues.
    """
    logger.info(f"Validating book structure: {path}")
    # TODO: Implementation in US4 (CLI Command Structure)
    typer.echo("Validate command placeholder - implementation coming in Phase 3")


@app.command()
def init(
    path: str = typer.Argument(
        ...,
        help="Path for new book project",
    ),
) -> None:
    """Initialize a new book project scaffold.

    Creates directory structure, sample files, and configuration.
    """
    logger.info(f"Initializing new book project: {path}")
    # TODO: Implementation in US4 (CLI Command Structure)
    typer.echo("Init command placeholder - implementation coming in Phase 3")


@app.command()
def config(
    path: str = typer.Option(
        "book.toml",
        "--path",
        "-p",
        help="Path to configuration file",
    ),
) -> None:
    """Show or validate configuration.

    Displays current configuration and validates schema.
    """
    logger.info(f"Loading configuration from: {path}")
    # TODO: Implementation in US5 (Configuration System)
    typer.echo("Config command placeholder - implementation coming in Phase 7")


if __name__ == "__main__":
    app()
