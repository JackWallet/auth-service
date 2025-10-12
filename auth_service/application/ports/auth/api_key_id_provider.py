from abc import abstractmethod
from dataclasses import dataclass

from application.ports.auth.id_provider import IdProvider
from domain.entities.api_key import APIKeyAccessLevelEnum, APIKeyStatusEnum


@dataclass(frozen=True, slots=True)
class ApiKeyIdProviderRequest:
    key_raw: str


@dataclass(frozen=True, slots=True)
class ApiKeyIdProviderResponce:
    key_status: APIKeyStatusEnum
    key_access_level: APIKeyAccessLevelEnum


class ApiKeyIdProvider(
    IdProvider[ApiKeyIdProviderRequest, ApiKeyIdProviderResponce | None],
):
    @abstractmethod
    async def get_user_acknowledgements(
        self,
        data: ApiKeyIdProviderRequest,
    ) -> ApiKeyIdProviderResponce | None:
        raise NotImplementedError
