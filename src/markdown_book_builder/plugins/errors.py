"""Plugin system exceptions."""


class PluginError(Exception):
    """Base exception for plugin system errors."""

    pass


class PluginNotFoundError(PluginError):
    """Raised when a requested plugin is not registered."""

    pass
