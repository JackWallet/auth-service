from abc import ABC, abstractmethod

from domain.entities.api_key import APIKey


class APIKeyEncryption(ABC):
    @abstractmethod
    def encrypt(self, key: APIKey) -> None:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, key: APIKey) -> None:
        raise NotImplementedError
