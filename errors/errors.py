class AppError(Exception):
    pass


class ConfigError(AppError):
    pass


class APIError(AppError):
    pass


class JsonError(AppError):
    pass


class ResponseDataTypeError(AppError):
    pass
