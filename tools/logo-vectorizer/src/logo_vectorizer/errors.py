"""Public exceptions for configuration and execution failures."""


class ConfigurationError(ValueError):
    """A supplied configuration value violates the public contract."""


class VectorizationError(RuntimeError):
    """An execution stage failed; the original exception remains its cause."""
