from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from domain.api_key_id import ApiKeyId


class APIKeyAccessLevelEnum(StrEnum):
    READ = "read"
    WRITE = "write"


class APIKeyStatusEnum(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass(slots=True)
class APIKey:
    key_id: ApiKeyId | None
    key: str
    access_level: APIKeyAccessLevelEnum
    status: APIKeyStatusEnum
    created_at: datetime
    last_accessed: datetime

    @classmethod
    def create(
        cls,
        key: str,
        access_level: APIKeyAccessLevelEnum = APIKeyAccessLevelEnum.READ,
    ) -> "APIKey":
        now = datetime.now(tz=UTC)
        return cls(
            key_id=None,
            key=key,
            access_level=access_level,
            status=APIKeyStatusEnum.ACTIVE,
            created_at=now,
            last_accessed=now,
        )
