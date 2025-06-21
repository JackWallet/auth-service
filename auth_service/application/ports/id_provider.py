from abc import ABC, abstractmethod
from typing import Generic, TypeVar

OutputDTO = TypeVar("OutputDTO")
InputDTO = TypeVar("InputDTO")


class IdProvider(ABC, Generic[InputDTO, OutputDTO]):
    @abstractmethod
    def get_user_acknowledgements(self, data: InputDTO) -> OutputDTO:
        raise NotImplementedError
