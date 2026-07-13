"""Main CLI application and root commands."""

import logging

import typer

from markdown_book_builder.cli.build import build
from markdown_book_builder.cli.config import config
from markdown_book_builder.cli.images import images_app
from markdown_book_builder.cli.init import init
from markdown_book_builder.cli.validate import validate
from markdown_book_builder.core.logging import get_logger, setup_logging

logger = get_logger(__name__)

app = typer.Typer(
    help="Markdown Book Builder: Convert Markdown collections into professional books",
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
        setup_logging(level=logging.DEBUG)


app.command()(build)
app.command()(validate)
app.command()(init)
app.command()(config)
app.add_typer(images_app, name="images")


if __name__ == "__main__":
    app()
