"""Entry point for Markdown Book Builder CLI.

Run with: python -m markdown_book_builder
"""

from markdown_book_builder.cli.main import app


def main() -> None:
    """Run the CLI application."""
    app()


if __name__ == "__main__":
    main()
