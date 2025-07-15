from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.database.repositories.api_key_repository import (
    ApiKeyWriterRepository,
)
from domain.entities.api_key import APIKey, APIKeyStatusEnum
from infrastructure.persistence_sqla.mappings.api_key import api_keys_table


class SQLAlchemyApiKeywriterRepository(ApiKeyWriterRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_api_key(self, api_key: APIKey) -> None:
        self._session.add(api_key)

    async def revoke_api_key(self, key: str) -> None:
        query = (
            update(APIKey)
            .where(api_keys_table.c.key == key)
            .values(status=APIKeyStatusEnum.REVOKED)
        )
        await self._session.execute(query)
