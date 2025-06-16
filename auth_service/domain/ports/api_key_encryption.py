from abc import ABC, abstractmethod


class APIKeyEncryption(ABC):
    @abstractmethod
    def encrypt(self, key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, key: str) -> str:
        raise NotImplementedError
