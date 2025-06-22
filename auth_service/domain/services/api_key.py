from datetime import UTC, datetime

from domain.entities.api_key import (
    APIKey,
    APIKeyAccessLevelEnum,
    APIKeyStatusEnum,
)
from domain.ports.api_key_generator import APIKeyGenerator


class APIKeyService:
    def __init__(
        self,
        key_generator: APIKeyGenerator,
    ) -> None:
        self._key_generator = key_generator

    def create(self) -> APIKey:
        now = datetime.now(tz=UTC)
        key_raw = self._key_generator.generate_key()

        return APIKey(
            key_id=None,
            key=key_raw,
            access_level=APIKeyAccessLevelEnum.READ,
            status=APIKeyStatusEnum.ACTIVE,
            created_at=now,
            last_accessed=now,
        )
