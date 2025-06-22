class ApplicationError(Exception):
    pass


class InsufficientPrivilegesError(ApplicationError):
    def __init__(self, access_level_required: str) -> None:
        super().__init__(
            f"You need {access_level_required} \
                access level to perform this operation",
        )


class AuthenticationError(ApplicationError):
    pass


class ApiKeyExpiredError(AuthenticationError):
    def __init__(self, api_key_raw: str) -> None:
        super().__init__(
            f"Api Key {api_key_raw} has been expired",
        )


class ApiKeyRevokedError(AuthenticationError):
    def __init__(self, api_key_raw: str) -> None:
        super().__init__(
            f"Api Key {api_key_raw} has been revoked",
        )


class ApiKeyNotFoundError(AuthenticationError):
    def __init__(self, api_key_raw: str) -> None:
        super().__init__(
            f"Api Key {api_key_raw} doesn't exist",
        )
