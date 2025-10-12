from application.exceptions.base import ApplicationError


class AuthError(ApplicationError):
    pass


class InsufficientPrivilegesAuthError(AuthError):
    def __init__(self, raw_key: str, access_level_required: str) -> None:
        super().__init__(
            f"Key {raw_key} need {access_level_required} \
                access level to perform this operation",
        )


class ApiKeyExpiredAuthError(AuthError):
    def __init__(self, raw_key: str) -> None:
        super().__init__(
            f"Api Key {raw_key} has been expired",
        )


class ApiKeyRevokedAuthError(AuthError):
    def __init__(self, raw_key: str) -> None:
        super().__init__(
            f"Api Key {raw_key} has been revoked",
        )


class ApiKeyNotFoundAuthError(AuthError):
    def __init__(self, raw_key: str) -> None:
        super().__init__(
            f"Api Key {raw_key} doesn't exist",
        )
