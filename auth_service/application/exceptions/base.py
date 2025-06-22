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
    def __init__(self) -> None:
        super().__init__(
            "Api Key has been expired",
        )


class ApiKeyRevokedError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__(
            "Api Key has been revoked",
        )


class ApiKeyNotFoundError(AuthenticationError):
    def __init__(self) -> None:
        super().__init__(
            "Api Key doesn't exist",
        )
