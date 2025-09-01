import logging
from typing import Annotated

from dishka import FromDishka
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.exceptions.api_key import ApiKeyNotFoundError
from application.exceptions.auth import ApiKeyNotFoundAuthError
from application.interactors.get_key_by_body import (
    GetKeyByBody,
    GetKeyByBodyRequest,
)
from domain.entities.api_key import (
    APIKey,
)
from presentation.auth.service import is_active, is_allowed_to_write

logger = logging.getLogger(__name__)

api_key_scheme = HTTPBearer()


async def get_current_api_key(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Security(api_key_scheme),
    ],
    interactor: FromDishka[GetKeyByBody],
) -> APIKey:
    api_key_raw = credentials.credentials
    request = GetKeyByBodyRequest(key_raw=api_key_raw)
    try:
        logger.debug("Trying to find %s", api_key_raw)
        api_key = await interactor(data=request)
    except ApiKeyNotFoundError as e:
        logger.debug("Api key %s was not found", api_key_raw)
        raise ApiKeyNotFoundAuthError(raw_key=api_key_raw) from e
    else:
        logger.debug("Found key %s", api_key_raw)
        return api_key.key


async def requires_read_access(
    api_key: Annotated[APIKey, Security(get_current_api_key)],
) -> APIKey:
    is_active(api_key)
    return api_key


async def requires_write_access(
    api_key: Annotated[APIKey, Security(get_current_api_key)],
) -> APIKey:
    is_active(api_key)
    is_allowed_to_write(api_key)
    return api_key
