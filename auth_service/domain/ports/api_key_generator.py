from abc import ABC, abstractmethod


class APIKeyGenerator(ABC):
    @abstractmethod
    def generate_key(self) -> str:
        raise NotImplementedError
