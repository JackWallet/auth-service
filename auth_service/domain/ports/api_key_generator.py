from abc import abstractmethod
from typing import Generic, Protocol, TypeVar

SecretKey = TypeVar("SecretKey")


class APIKeyGenerator(Protocol, Generic[SecretKey]):
    @abstractmethod
    def generate_key(self) -> SecretKey:
        pass
