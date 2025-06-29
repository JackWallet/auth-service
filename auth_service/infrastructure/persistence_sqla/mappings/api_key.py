from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Table,
    func,
)

from domain.entities.api_key import APIKeyAccessLevelEnum, APIKeyStatusEnum
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
        "created",
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
