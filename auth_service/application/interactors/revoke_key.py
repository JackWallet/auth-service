import logging
from dataclasses import dataclass

from application.exceptions.auth import (
    ApiKeyNotFoundAuthError,
    ApiKeyRevokedAuthError,
    InsufficientPrivilegesAuthError,
)
from application.exceptions.validation import (
    ApiKeyExpiredValidationError,
    ApiKeyRevokedValidationError,
    InsufficientPrivilegesValidationError,
)
from application.ports.access_validator import AccessValidator
from application.ports.auth.api_key_id_provider import (
    ApiKeyIdProvider,
    ApiKeyIdProviderRequest,
)
from application.ports.database.repositories.api_key_repository import (
    ApiKeyWriterRepository,
)
from application.ports.interactor import Interactor
from domain.entities.api_key import APIKeyAccessLevelEnum

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RevokeKeyRequest:
    key: str
    request_from_api_key_raw: str


class RevokeKey(Interactor[RevokeKeyRequest, None]):
    def __init__(
        self,
        api_key_writer: ApiKeyWriterRepository,
        id_provider: ApiKeyIdProvider,
        access_validator: AccessValidator,
    ) -> None:
        self._api_key_writer = api_key_writer
        self._id_provider = id_provider
        self._api_key_validator = access_validator

    async def __call__(self, data: RevokeKeyRequest) -> None:
        id_provider_responce = (
            await self._id_provider.get_user_acknowledgements(
                data=ApiKeyIdProviderRequest(
                    key_raw=data.request_from_api_key_raw,
                ),
            )
        )
        if id_provider_responce is None:
            raise ApiKeyNotFoundAuthError(
                raw_key=data.request_from_api_key_raw,
            )
        try:
            self._api_key_validator.validate_access_level(
                input_access_level=id_provider_responce.key_access_level,
                target_access_level=APIKeyAccessLevelEnum.WRITE,
            )
        except InsufficientPrivilegesValidationError as validation_err:
            insuf_priveleges_auth_err = InsufficientPrivilegesAuthError(
                raw_key=data.request_from_api_key_raw,
                access_level_required=APIKeyAccessLevelEnum.WRITE,
            )
            logger.info(str(insuf_priveleges_auth_err))
            raise insuf_priveleges_auth_err from validation_err

        try:
            self._api_key_validator.validate_access_status(
                api_key_status=id_provider_responce.key_status,
            )
        except ApiKeyRevokedValidationError as validation_err:
            key_revoked_auth_err = ApiKeyRevokedAuthError(
                raw_key=data.request_from_api_key_raw,
            )
            logger.info(str(key_revoked_auth_err))
            raise key_revoked_auth_err from validation_err
        except ApiKeyExpiredValidationError as validation_err:
            key_expired_auth_err = ApiKeyRevokedAuthError(
                raw_key=data.request_from_api_key_raw,
            )
            logger.info(str(key_expired_auth_err))
            raise key_expired_auth_err from validation_err
