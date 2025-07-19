from types import MappingProxyType
from typing import Final

from fastapi import status
from pydantic import ValidationError

from application.exceptions.api_key import ApiKeyNotFoundError
from application.exceptions.auth import (
    ApiKeyExpiredAuthError,
    ApiKeyNotFoundAuthError,
    ApiKeyRevokedAuthError,
    InsufficientPrivilegesAuthError,
)
from application.exceptions.base import ApplicationError
from domain.exceptions.base import DomainError

EXCEPTION_MAPPING_PROXY: Final[MappingProxyType[type[Exception], int]] = (
    MappingProxyType(
        {
            ApiKeyNotFoundError: status.HTTP_404_NOT_FOUND,
            ApiKeyExpiredAuthError: status.HTTP_401_UNAUTHORIZED,
            ApiKeyRevokedAuthError: status.HTTP_401_UNAUTHORIZED,
            ApiKeyNotFoundAuthError: status.HTTP_401_UNAUTHORIZED,
            InsufficientPrivilegesAuthError: status.HTTP_403_FORBIDDEN,
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            DomainError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            ApplicationError: status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )
)
