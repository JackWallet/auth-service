class ApplicationError(Exception):
    pass


class InsufficientPrivilegesError(ApplicationError):
    pass


class AuthenticationError(InsufficientPrivilegesError):
    pass


class ApiKeyExpiredError(AuthenticationError):
    pass


class ApiKeyRevokedError(AuthenticationError):
    pass
