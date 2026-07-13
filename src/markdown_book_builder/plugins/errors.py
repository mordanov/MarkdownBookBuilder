"""Plugin system exceptions."""


class PluginError(Exception):
    """Base exception for plugin system errors."""

    pass


class PluginNotFoundError(PluginError):
    """Raised when a requested plugin is not registered."""

    pass


class PluginLoadError(PluginError):
    """Raised when a plugin fails to load or register."""

    pass
