import logging
from dataclasses import dataclass
from datetime import datetime

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
from domain.services.api_key import APIKeyService

logger = logging.getLogger(__name__)


# Slots makes it impossible for this dataclass to obtain any new attributes
@dataclass(frozen=True, slots=True)
class IssueKeyRequest:  # type:ignore[misc]
    api_key_access_level: APIKeyAccessLevelEnum
    status: APIKeyStatusEnum
    created_at: datetime
    last_accessed: datetime
    request_access_level: APIKeyAccessLevelEnum


@dataclass(frozen=True, slots=True)
class IssueKeyResult:  # type:ignore[misc]
    key: str
    access_level: APIKeyAccessLevelEnum


class IssueKey(Interactor[IssueKeyRequest, IssueKeyResult]):
    def __init__(
        self,
        api_key_writer: ApiKeyWriterRepository,
        transaction_manager: TransactionManager,
        api_key_service: APIKeyService,
    ) -> None:
        self._api_key_writer = api_key_writer
        self._transaction_manager = transaction_manager
        self._api_key_service = api_key_service

    def __call__(self, data: IssueKeyRequest) -> IssueKeyResult:
        api_key = self._api_key_service.create(access_level=data.access_level)
        self._api_key_writer.add_api_key(api_key=api_key)
        await self._transaction_manager.commit()
        return IssueKeyResult()
