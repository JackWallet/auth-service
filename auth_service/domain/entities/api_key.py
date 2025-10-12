from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum

from domain.entities.api_key_id import APIKeyId


class APIKeyAccessLevelEnum(StrEnum):
    READ = "read"
    WRITE = "write"


class APIKeyStatusEnum(StrEnum):
    ACTIVE = "active"
    REVOKED = "revoked"
    EXPIRED = "expired"


@dataclass(slots=True)
class APIKey:
    key_id: APIKeyId | None
    key: str
    access_level: APIKeyAccessLevelEnum
    status: APIKeyStatusEnum
    created_at: datetime
    last_accessed: datetime
