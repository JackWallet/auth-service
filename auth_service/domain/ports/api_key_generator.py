from abc import ABC, abstractmethod
from typing import Generic

from domain.ports.api_key_type import SecretKey


class APIKeyGenerator(ABC, Generic[SecretKey]):
    @abstractmethod
    def generate_key(self) -> SecretKey:
        raise NotImplementedError
