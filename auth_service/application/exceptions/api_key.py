from application.exceptions.base import ApplicationError


class ApiKeyOperationError(ApplicationError):
    pass


class ApiKeyNotFoundError(ApplicationError):
    pass


class ApiKeyRevokedError(ApplicationError):
    pass


class ApiKeyExpiredError(ApplicationError):
    pass
