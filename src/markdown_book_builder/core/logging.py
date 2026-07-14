"""Logging configuration for CLI and library usage."""

import logging
import sys

_PACKAGE = "markdown_book_builder"


def setup_logging(debug: bool = False, verbose: bool = False) -> None:
    """Configure logging for CLI output.

    Levels:
        (default) INFO   — progress messages only
        --debug          — DEBUG for this package (chapters, images, errors)
        --verbose        — DEBUG for everything incl. httpx/openai API calls
    """
    root = logging.getLogger()

    # Remove any existing handlers
    for h in root.handlers[:]:
        root.removeHandler(h)

    handler = logging.StreamHandler(sys.stderr)

    if verbose:
        # Full debug: all loggers including third-party (API calls, httpx, etc.)
        root.setLevel(logging.DEBUG)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
            datefmt="%H:%M:%S",
        )
    elif debug:
        # Package-only debug: suppress noisy third-party libs
        root.setLevel(logging.WARNING)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")
        # Bring our own package down to DEBUG
        logging.getLogger(_PACKAGE).setLevel(logging.DEBUG)
    else:
        root.setLevel(logging.WARNING)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(fmt="%(levelname)s: %(message)s")
        logging.getLogger(_PACKAGE).setLevel(logging.INFO)

    handler.setFormatter(formatter)
    root.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
