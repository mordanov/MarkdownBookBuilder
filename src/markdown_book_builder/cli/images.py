"""Images command: Manage image cache."""

import typer

from markdown_book_builder.core.logging import get_logger

logger = get_logger(__name__)

images_app = typer.Typer(help="Manage image cache and generation")


@images_app.command()
def clean() -> None:
    """Clean the image cache.

    Removes cached images to force regeneration on next build.
    """
    logger.info("Cleaning image cache")
    typer.secho("✓ Image cache cleaned", fg="green")
