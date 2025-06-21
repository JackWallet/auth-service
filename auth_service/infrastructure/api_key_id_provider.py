from dataclasses import dataclass

from application.ports.auth.id_provider import IdProvider
from application.ports.database.repositories.api_key_repository import (
    ApiKeyReaderRepository,
)
from domain.entities.api_key import APIKeyAccessLevelEnum, APIKeyStatusEnum
from domain.ports.api_key_encryption import APIKeyEncryption


@dataclass(frozen=True, slots=True)
class ApiKeyIdProviderRequest:
    key_raw: str


@dataclass(frozen=True, slots=True)
class ApiKeyIdProviderResponce:
    key_status: APIKeyStatusEnum
    key_access_level: APIKeyAccessLevelEnum


class ApiKeyIdProvider(
    IdProvider[ApiKeyIdProviderRequest, ApiKeyIdProviderResponce],
):
    def __init__(
        self,
        api_key_reader: ApiKeyReaderRepository,
        api_key_encryption: APIKeyEncryption,
    ) -> None:
        self._api_key_reader = api_key_reader
        self._api_key_encryption = api_key_encryption

    async def get_user_acknowledgements(
        self,
        data: ApiKeyIdProviderRequest,
    ) -> ApiKeyIdProviderResponce:
        key_value = self._api_key_encryption.encrypt(key=data.key_raw)
        api_key = await self._api_key_reader.get_key_by_key_value(
            key_value=key_value,
        )

        return ApiKeyIdProviderResponce(
            key_access_level=api_key.access_level,
            key_status=api_key.status,
        )
