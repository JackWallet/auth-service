from dataclasses import dataclass

from domain.value_objects.base import ValueObject


@dataclass(frozen=True)
class ApiKeyId(ValueObject):
    id: int
