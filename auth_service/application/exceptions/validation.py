from application.exceptions.base import ApplicationError


class ValidationError(ApplicationError):
    pass


class InsufficientPrivilegesValidationError(ValidationError):
    def __init__(self, access_level_required: str) -> None:
        super().__init__(
            f"You need {access_level_required} \
                access level to perform this operation",
        )


class ApiKeyExpiredValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Api Key has been expired",
        )


class ApiKeyRevokedValidationError(ValidationError):
    def __init__(self) -> None:
        super().__init__(
            "Api Key has been revoked",
        )
