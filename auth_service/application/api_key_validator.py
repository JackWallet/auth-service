from application.exceptions.validation import (
    ApiKeyExpiredValidationError,
    ApiKeyRevokedValidationError,
    InsufficientPrivilegesValidationError,
)
from application.ports.access_validator import AccessValidator
from domain.entities.api_key import APIKeyAccessLevelEnum, APIKeyStatusEnum


class ApiKeyValidator(AccessValidator):
    @staticmethod
    def validate_access_level(
        input_access_level: APIKeyAccessLevelEnum,
        target_access_level: APIKeyAccessLevelEnum,
    ) -> None:
        if (
            input_access_level is APIKeyAccessLevelEnum.WRITE
            and target_access_level is APIKeyAccessLevelEnum.READ
        ):
            raise InsufficientPrivilegesValidationError(
                access_level_required=target_access_level,
            )

    @staticmethod
    def validate_access_status(api_key_status: APIKeyStatusEnum) -> None:
        if api_key_status is APIKeyStatusEnum.EXPIRED:
            raise ApiKeyExpiredValidationError
        if api_key_status is APIKeyStatusEnum.REVOKED:
            raise ApiKeyRevokedValidationError
