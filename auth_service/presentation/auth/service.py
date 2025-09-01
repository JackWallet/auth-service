import logging

from application.exceptions.auth import (
    ApiKeyExpiredAuthError,
    ApiKeyRevokedAuthError,
    InsufficientPrivilegesAuthError,
)
from domain.entities.api_key import (
    APIKey,
    APIKeyAccessLevelEnum,
    APIKeyStatusEnum,
)

logger = logging.getLogger(__name__)


def is_active(key: APIKey) -> None:
    if key.status is APIKeyStatusEnum.EXPIRED:
        logger.debug("Api key %s is expired")
        raise ApiKeyExpiredAuthError(raw_key=key.key)
    if key.status is APIKeyStatusEnum.REVOKED:
        logger.debug("Api key %s is revoked")
        raise ApiKeyRevokedAuthError(raw_key=key.key)


def is_allowed_to_write(key: APIKey) -> None:
    if key.access_level is not APIKeyAccessLevelEnum.WRITE:
        raise InsufficientPrivilegesAuthError(
            raw_key=key.key, access_level_required=APIKeyAccessLevelEnum.WRITE,
        )
