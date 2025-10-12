from abc import ABC, abstractmethod


class APIKeyEncryption(ABC):
    @abstractmethod
    def encrypt(self, key_raw: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def decrypt(self, key_raw: str) -> str:
        raise NotImplementedError
