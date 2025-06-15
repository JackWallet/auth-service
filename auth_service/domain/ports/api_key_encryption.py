from abc import abstractmethod
from typing import Protocol


class APIKeyEncryption(Protocol):
    @abstractmethod
    def encrypt(self, key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, key: str) -> str:
        raise NotImplementedError
