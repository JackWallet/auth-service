from dataclasses import dataclass
from datetime import datetime

from application.abstract.database.repositories.api_key_repository import (
    ApiKeyWriterRepository,
)
from application.abstract.database.secret_generator import (
    SecretGenerator,
)
from application.abstract.database.transaction_manager import (
    TransactionManager,
)
from application.abstract.interactor import Interactor
from domain.api_key import APIKey, APIKeyAccessLevelEnum, APIKeyStatusEnum


# Slots makes it impossible for this dataclass to obtain any new attributes
@dataclass(frozen=True, slots=True)
class AddKeyDTO:
    access_level: APIKeyAccessLevelEnum
    status: APIKeyStatusEnum
    created_at: datetime
    last_accessed: datetime


@dataclass(frozen=True, slots=True)
class AddKeyResultDTO:
    key: str


class AddKey(Interactor[AddKeyDTO, None]):
    def __init__(
        self,
        api_key_writer: ApiKeyWriterRepository,
        transaction_manager: TransactionManager,
        secret_generator: SecretGenerator,
    ) -> None:
        self._api_key_writer = api_key_writer
        self._transaction_manager = transaction_manager
        self._secret_generator = secret_generator

    def __call__(self, data: AddKeyDTO) -> None:
        ...
