import os
from typing import NewType, cast

from pydantic import BaseModel, Field, PostgresDsn, field_validator
from pydantic.networks import IPvAnyAddress

from entrypoint.error import MissingConfigVariableError
from entrypoint.logging.logs import LoggingLevel

PostgresSettingsDsn = NewType("PostgresSettingsDsn", str)


def get_str_from_env(key: str) -> str:
    if value := os.getenv(key):
        return value
    raise MissingConfigVariableError(variable_name=key)


class PostgresSettings(BaseModel):
    user: str = Field(alias="USER")
    password: str = Field(alias="PASSWORD")
    db: str = Field(alias="DB")
    host: IPvAnyAddress = Field(alias="HOST")
    port: int = Field(alias="PORT")
    driver: str = Field(alias="DRIVER")

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        if not 1 <= v <= 65535:  # noqa: PLR2004
            msg = "Invalid postgres port was provided"
            raise ValueError(msg)
        return v

    @property
    def dsn(self) -> str:
        return cast(
            "PostgresSettingsDsn",
            str(
                PostgresDsn.build(
                    scheme=f"postgresql+{self.driver}",
                    username=self.user,
                    password=self.password,
                    host=str(self.host),
                    port=self.port,
                    path=self.db,
                ),
            ),
        )


class LoggingLevelSettings(BaseModel):
    logging_level: LoggingLevel = Field(alias="LOGGING_LEVEL")


class FernetKeySettings(BaseModel):
    fernet_key: str = Field(alias="FERNET_KEY_BASE64")

    @classmethod
    def from_env(cls) -> "FernetKeySettings":
        return FernetKeySettings(
            FERNET_KEY_BASE64=get_str_from_env("FERNET_KEY_BASE64"),
        )
