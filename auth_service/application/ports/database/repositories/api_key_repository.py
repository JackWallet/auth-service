from abc import abstractmethod
from typing import Protocol

from domain.entities.api_key import APIKey


class ApiKeyReaderRepository(Protocol):
    @abstractmethod
    async def is_allowed_to_read(self, key_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def is_allowed_to_write(self, key_id: str) -> bool:
        raise NotImplementedError


class ApiKeyWriterRepository(Protocol):
    @abstractmethod
    async def add_api_key(self, api_key: APIKey) -> None:
        raise NotImplementedError

    @abstractmethod
    async def revoke_api_key(self, key: str) -> None:
        raise NotImplementedError
