from abc import ABC, abstractmethod
from typing import Generic, TypeVar

InputDTO = TypeVar("InputDTO")
OutputDTO = TypeVar("OutputDTO")


class SecretGenerator(ABC, Generic[OutputDTO]):
    @abstractmethod
    def generate_secret(self) -> OutputDTO:
        raise NotImplementedError
