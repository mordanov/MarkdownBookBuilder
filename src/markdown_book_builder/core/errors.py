"""Custom exception hierarchy for Markdown Book Builder."""


class BookBuilderError(Exception):
    """Base exception for all Markdown Book Builder errors."""

    pass


class ConfigurationError(BookBuilderError):
    """Raised when configuration loading or validation fails."""

    pass


class DiscoveryError(BookBuilderError):
    """Raised when document discovery or metadata extraction fails."""

    pass


class ValidationError(BookBuilderError):
    """Raised when AST validation or document validation fails."""

    pass


class CLIError(BookBuilderError):
    """Raised when CLI command execution fails."""

    pass


class TransformationError(BookBuilderError):
    """Raised when AST transformation fails."""

    pass
