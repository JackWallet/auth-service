from fastapi import HTTPException, Request, status

from application.exceptions.auth import (
    ApiKeyExpiredAuthError,
    ApiKeyNotFoundAuthError,
    ApiKeyRevokedAuthError,
    InsufficientPrivilegesAuthError,
)


def unauthorized_exception_handler(
    request: Request,
    exc: ApiKeyNotFoundAuthError,
) -> None:
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="This key doesn't exist",
    )


def key_expired_exception_handler(
    request: Request,
    exc: ApiKeyExpiredAuthError,
) -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This key is expired",
    )


def key_revoked_exception_handler(
    request: Request,
    exc: ApiKeyRevokedAuthError,
) -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This key is revoked",
    )


def insufficient_privileges_exception_handler(
    request: Request,
    exc: InsufficientPrivilegesAuthError,
) -> None:
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="This operation requires elevation",
    )
