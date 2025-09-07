from dishka import FromDishka
from fastapi import APIRouter, Security
from pydantic import BaseModel

from application.interactors.get_key_by_body import (
    GetKeyByBody,
    GetKeyByBodyRequest,
)
from domain.entities.api_key import APIKey
from presentation.auth.api_key_auth import requires_read_access

api_key_reader_router = APIRouter()


class GetApiKeyRequestModel(BaseModel):
    key_raw: str


class GetApiKeyResponce(BaseModel):
    key: APIKey


@api_key_reader_router.get(
    path="/",
    dependencies=[Security(requires_read_access)],
)
async def get_api_key(
    interactor: FromDishka[GetKeyByBody],
    request: GetApiKeyRequestModel,
) -> GetApiKeyResponce:
    request_data = GetKeyByBodyRequest(key_raw=request.key_raw)
    response = await interactor(data=request_data)
    return GetApiKeyResponce(key=response.key)
