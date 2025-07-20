import logging
from typing import Annotated

from dishka import FromDishka
from fastapi import Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.exceptions.auth import ApiKeyNotFoundAuthError
from application.ports.auth.api_key_id_provider import (
    ApiKeyIdProvider,
    ApiKeyIdProviderRequest,
    ApiKeyIdProviderResponce,
)

logger = logging.getLogger(__name__)

api_key_scheme = HTTPBearer()


async def get_current_api_key(
    credentials: Annotated[
        HTTPAuthorizationCredentials,
        Security(api_key_scheme),
    ],
    interactor: FromDishka[ApiKeyIdProvider],
) -> ApiKeyIdProviderResponce:
    api_key_raw = credentials.credentials
    request = ApiKeyIdProviderRequest(key_raw=api_key_raw)
    try:
        logger.debug("Trying to authenticate key %s", api_key_raw)
        return interactor.get_user_acknowledgements(data=request)
    except ApiKeyNotFoundAuthError:
        logger.debug("Api key %s was never found", api_key_raw)
        raise
