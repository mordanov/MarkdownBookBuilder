"""Main CLI application and root commands."""

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
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        help="Debug output: chapters, image generation, errors (package logs only)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Verbose debug: API calls, warnings, all debug info (includes third-party libs)",
    ),
) -> None:
    """Main entry point for Markdown Book Builder CLI."""
    setup_logging(debug=debug, verbose=verbose)


app.command()(build)
app.command()(validate)
app.command()(init)
app.command()(config)
app.add_typer(images_app, name="images")


if __name__ == "__main__":
    app()
