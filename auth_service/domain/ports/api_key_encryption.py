from abc import ABC, abstractmethod
from typing import Generic

from domain.ports.api_key_type import SecretKey


class APIKeyEncryption(ABC, Generic[SecretKey]):
    @abstractmethod
    def encrypt(self, key: str) -> SecretKey:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, key: str) -> SecretKey:
        raise NotImplementedError
