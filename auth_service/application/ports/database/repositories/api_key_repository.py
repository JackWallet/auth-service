from abc import abstractmethod
from typing import Protocol

from domain.api_key import APIKey


class ApiKeyReaderRepository(Protocol):
    @abstractmethod
    def is_allowed_to_read(self, key_id: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def is_allower_to_write(self, key_id: str) -> bool:
        raise NotImplementedError


class ApiKeyWriterRepository(Protocol):
    @abstractmethod
    def add_api_key(self, api_key: APIKey) -> None:
        raise NotImplementedError

    @abstractmethod
    def revoke_api_key(self, key: str) -> None:
        raise NotImplementedError
