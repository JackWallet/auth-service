class ApplicationError(Exception):
    pass


class InsufficientPrivilegesError(ApplicationError):
    pass


class AuthenticationError(ApplicationError):
    pass


class ApiKeyExpiredError(AuthenticationError):
    pass


class ApiKeyRevokedError(AuthenticationError):
    pass


class ApiKeyNotFoundError(AuthenticationError):
    pass
