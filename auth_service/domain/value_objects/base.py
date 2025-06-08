from abc import ABC
from dataclasses import asdict, dataclass, fields
from typing import Any

from domain.exceptions.base import DomainFieldValidationError


@dataclass(frozen=True)
class ValueObject(ABC):
    def __post_init__(self) -> None:
        if len(fields(self)) < 1:
            msg = f"{type(self).__name__} can't have less than one attribute"
            raise DomainFieldValidationError(msg)

    def get_fields(self) -> dict[str, Any]:
        return asdict(self)
