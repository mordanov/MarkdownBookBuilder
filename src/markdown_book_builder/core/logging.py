"""Logging configuration for CLI and library usage."""

import logging
import sys


def setup_logging(level: int = logging.INFO, verbose: bool = False) -> None:
    """Set up logging for CLI output.

    Args:
        level: Logging level (default: INFO)
        verbose: Enable verbose output (DEBUG level)
    """
    if verbose:
        level = logging.DEBUG

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create console handler with CLI-appropriate formatting
    handler = logging.StreamHandler(sys.stderr)
    handler.setLevel(level)

    # Use simple format for CLI
    formatter = logging.Formatter(
        fmt="%(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance.

    Args:
        name: Logger name (typically __name__)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
