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
from application.ports.database.transaction_manager import (
    TransactionManager,
)
from application.ports.interactor import Interactor
from domain.entities.api_key import (
    APIKeyAccessLevelEnum,
)
from domain.ports.api_key_encryption import APIKeyEncryption
from domain.services.api_key import APIKeyService

logger = logging.getLogger(__name__)


# Slots makes it impossible for this dataclass to obtain any new attributes
@dataclass(frozen=True, slots=True)
class IssueKeyRequest:  # type:ignore[misc]
    request_from_api_key_raw: str


@dataclass(frozen=True, slots=True)
class IssueKeyResult:  # type:ignore[misc]
    key: str


class IssueKey(Interactor[IssueKeyRequest, IssueKeyResult]):
    def __init__(  # noqa: PLR0913
        self,
        api_key_writer: ApiKeyWriterRepository,
        transaction_manager: TransactionManager,
        api_key_encryption: APIKeyEncryption,
        api_key_service: APIKeyService,
        access_validator: AccessValidator,
        id_provider: ApiKeyIdProvider,
    ) -> None:
        self._api_key_writer = api_key_writer
        self._transaction_manager = transaction_manager
        self._api_key_service = api_key_service
        self._id_provider = id_provider
        self._api_key_validator = access_validator
        self._api_key_encryption = api_key_encryption

    async def __call__(self, data: IssueKeyRequest) -> IssueKeyResult:
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

        api_key = self._api_key_service.create()
        key_raw = api_key.key
        api_key.key = self._api_key_encryption.encrypt(key_raw=key_raw)
        await self._api_key_writer.add_api_key(api_key=api_key)
        await self._transaction_manager.commit()
        return IssueKeyResult(key=key_raw)
