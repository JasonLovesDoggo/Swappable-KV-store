class DatabaseNotFoundError(NotImplementedError):
    pass


class InvalidConfigurationError(ValueError):  # the configuration is invalid
    pass
