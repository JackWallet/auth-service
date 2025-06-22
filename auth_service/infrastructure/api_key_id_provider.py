from application.ports.auth.api_key_id_provider import (
    ApiKeyIdProvider,
    ApiKeyIdProviderRequest,
    ApiKeyIdProviderResponce,
)
from application.ports.database.repositories.api_key_repository import (
    ApiKeyReaderRepository,
)
from domain.ports.api_key_encryption import APIKeyEncryption


class ApiKeyIdProviderImpl(
    ApiKeyIdProvider,
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
        key_value = self._api_key_encryption.encrypt(key_raw=data.key_raw)
        api_key = await self._api_key_reader.get_key_by_key_value(
            key_value=key_value,
        )

        return ApiKeyIdProviderResponce(
            key_access_level=api_key.access_level,
            key_status=api_key.status,
        )
