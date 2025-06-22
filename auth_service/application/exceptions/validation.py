from application.exceptions.base import ApplicationError


class ValidationError(ApplicationError):
    pass


class InsufficientPrivilegesError(ValidationError):
    def __init__(self, access_level_required: str) -> None:
        super().__init__(
            f"You need {access_level_required} \
                access level to perform this operation",
        )


class ApiKeyExpiredError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Api Key has been expired",
        )


class ApiKeyRevokedError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Api Key has been revoked",
        )


class ApiKeyNotFoundError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Api Key doesn't exist",
        )
