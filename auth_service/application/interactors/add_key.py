from dataclasses import dataclass
from datetime import datetime

from auth_service.domain.api_key import APIKeyAccessLevelEnum, APIKeyStatusEnum


# Slots makes it impossible for this dataclass to obtain any new attributes
@dataclass(frozen=True, slots=True)
class AddKeyDTO:
    key: str
    access_level: APIKeyAccessLevelEnum
    status: APIKeyStatusEnum
    created_at: datetime
    last_accessed: datetime
