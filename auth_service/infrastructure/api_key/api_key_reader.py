from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.database.repositories.api_key_repository import (
    ApiKeyReaderRepository,
)
from domain.entities.api_key import APIKey
from infrastructure.persistence_sqla.mappings.api_key import api_keys_table


class SQLAlchemyApiKeyReaderRepository(ApiKeyReaderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_key_by_key_value(self, key_value: str) -> APIKey | None:
        query = select(APIKey).where(api_keys_table.c.key == key_value)
        query_result = await self._session.execute(query)
        return query_result.scalar_one_or_none()
