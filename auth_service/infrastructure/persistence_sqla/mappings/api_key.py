from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Table,
    func,
)
from sqlalchemy.orm import composite

from domain.entities.api_key import (
    APIKey,
    APIKeyAccessLevelEnum,
    APIKeyStatusEnum,
)
from domain.entities.api_key_id import APIKeyId
from infrastructure.persistence_sqla.registry import mapping_registry

api_keys_table = Table(
    "api_keys",
    mapping_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("key", String, unique=True, nullable=False),
    Column(
        "access_level",
        Enum(APIKeyAccessLevelEnum),
        default=APIKeyAccessLevelEnum.READ,
        nullable=False,
    ),
    Column(
        "status",
        Enum(APIKeyStatusEnum),
        default=APIKeyStatusEnum.ACTIVE,
        nullable=False,
    ),
    Column(
        "created_at",
        DateTime,
        server_default=func.now(),
        nullable=False,
    ),
    Column(
        "last_accessed",
        DateTime,
        server_onupdate=func.now(),
        nullable=False,
    ),
)


def map_api_key_table() -> None:
    mapping_registry.map_imperatively(
        APIKey,
        api_keys_table,
        properties={
            "key_id": composite(APIKeyId, api_keys_table.c.id),
            "key": api_keys_table.c.key,
            "access_level": api_keys_table.c.access_level,
            "status": api_keys_table.c.status,
            "created_at": api_keys_table.c.created_at,
            "last_accessed": api_keys_table.c.last_accessed,
        },
    )
