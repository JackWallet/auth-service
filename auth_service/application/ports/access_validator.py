from abc import abstractmethod
from typing import Protocol

from domain.entities.api_key import APIKeyAccessLevelEnum, APIKeyStatusEnum


class AccessValidator(Protocol):
    @staticmethod
    @abstractmethod
    def validate_access_level(
        input_access_level: APIKeyAccessLevelEnum,
        target_access_level: APIKeyAccessLevelEnum,
    ) -> None:
        raise NotImplementedError

    @staticmethod
    @abstractmethod
    def validate_access_status(
        api_key_status: APIKeyStatusEnum,
    ) -> None:
        raise NotImplementedError
