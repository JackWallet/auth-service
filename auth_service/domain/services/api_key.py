from datetime import UTC, datetime

from domain.entities.api_key import (
    APIKey,
    APIKeyAccessLevelEnum,
    APIKeyStatusEnum,
)
from domain.ports.api_key_encryption import APIKeyEncryption
from domain.ports.api_key_generator import APIKeyGenerator
from domain.ports.api_key_type import SecretKey


class APIKeyService:
    def __init__(
        self,
        key_generator: APIKeyGenerator[SecretKey],
        key_encryption: APIKeyEncryption[SecretKey],
    ) -> None:
        self._key_generator = key_generator
        self._key_encryption = key_encryption

    def create(self, access_level: APIKeyAccessLevelEnum) -> APIKey:
        now = datetime.now(tz=UTC)
        key = self._key_generator.generate_key()
        return APIKey(
            key_id=None,
            key=str(key),
            access_level=access_level,
            status=APIKeyStatusEnum.ACTIVE,
            created_at=now,
            last_accessed=now,
        )
