from abc import abstractmethod
from typing import Protocol

from domain.entities.api_key import APIKey


class ApiKeyReaderRepository(Protocol):
    @abstractmethod
    async def get_key_by_key_value(self, key_id: str) -> APIKey:
        raise NotImplementedError


class ApiKeyWriterRepository(Protocol):
    @abstractmethod
    async def add_api_key(self, api_key: APIKey) -> None:
        raise NotImplementedError

    @abstractmethod
    async def revoke_api_key(self, key: str) -> None:
        raise NotImplementedError
