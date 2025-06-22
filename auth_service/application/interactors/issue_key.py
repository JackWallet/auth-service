import logging
from dataclasses import dataclass
from datetime import datetime

from application.exceptions.base import ApiKeyNotFoundError
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
    APIKeyStatusEnum,
)
from domain.entities.api_key_id import APIKeyId
from domain.services.api_key import APIKeyService

logger = logging.getLogger(__name__)


# Slots makes it impossible for this dataclass to obtain any new attributes
@dataclass(frozen=True, slots=True)
class IssueKeyRequest:  # type:ignore[misc]
    request_from_api_key_raw: str


@dataclass(frozen=True, slots=True)
class IssueKeyResult:  # type:ignore[misc]
    key: str
    key_id: APIKeyId


class IssueKey(Interactor[IssueKeyRequest, IssueKeyResult]):
    def __init__(
        self,
        api_key_writer: ApiKeyWriterRepository,
        transaction_manager: TransactionManager,
        api_key_service: APIKeyService,
        access_validator: AccessValidator,
        id_provider: ApiKeyIdProvider,
    ) -> None:
        self._api_key_writer = api_key_writer
        self._transaction_manager = transaction_manager
        self._api_key_service = api_key_service
        self._id_provider = id_provider
        self._api_key_validator = access_validator

    async def __call__(self, data: IssueKeyRequest) -> IssueKeyResult:
        id_provider_responce = (
            await self._id_provider.get_user_acknowledgements(
                data=ApiKeyIdProviderRequest(key_raw=data.request_api_key_raw),
            )
        )
        if id_provider_responce is None:
            raise ApiKeyNotFoundError

        self._api_key_validator.validate_access_level(
            input_access_level=id_provider_responce.key_access_level,
            target_access_level=APIKeyAccessLevelEnum.WRITE,
        )
        self._api_key_validator.validate_access_status(
            api_key_status=id_provider_responce.key_status
        )


        api_key = self._api_key_service.create()
        await self._api_key_writer.add_api_key(api_key=api_key)
        await self._transaction_manager.commit()
        return IssueKeyResult()
