import logging
from dataclasses import dataclass

from application.exceptions.api_key import ApiKeyNotFoundError
from application.ports.database.repositories.api_key_repository import (
    ApiKeyReaderRepository,
)
from application.ports.interactor import Interactor
from domain.entities.api_key import APIKey

logger = logging.getLogger(__name__)


# Type ignore as a result of mypy bug
@dataclass(frozen=True, slots=True)
class GetKeyByBodyRequest:  # type: ignore[misc]
    key_raw: str


@dataclass(frozen=True, slots=True)
class GetKeyByBodyResponce:  # type: ignore[misc]
    key: APIKey


class GetKeyByBody(Interactor[GetKeyByBodyRequest, GetKeyByBodyResponce]):
    def __init__(self, api_key_reader: ApiKeyReaderRepository) -> None:
        self._api_key_reader = api_key_reader

    async def __call__(
        self,
        data: GetKeyByBodyRequest,
    ) -> GetKeyByBodyResponce:
        api_key: (
            APIKey | None
        ) = await self._api_key_reader.get_key_by_key_value(
            key_value=data.key_raw,
        )
        if api_key is None:
            logger.debug("Api key %s doesn't exist", data.key_raw)
            raise ApiKeyNotFoundError
        return GetKeyByBodyResponce(key=api_key)
