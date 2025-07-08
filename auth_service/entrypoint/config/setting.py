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

    @field_validator("port", mode="before")
    @classmethod
    def validate_port(cls, v: int | str) -> int:
        if isinstance(v, str) and v.isnumeric() is False:
            msg = "Postgres port should be a number"
            raise ValueError(msg)
        v = int(v)

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

    @classmethod
    def from_env(cls) -> "PostgresSettings":
        return cls(
            USER=get_str_from_env("POSTGRES_USER"),
            PASSWORD=get_str_from_env("POSTGRES_PASSWORD"),
            DB=get_str_from_env("POSTGRES_DB_NAME"),
            HOST=get_str_from_env("POSTGRES_HOST"),  # type: ignore[arg-type] # Pydantic-side validation
            PORT=get_str_from_env("POSTGRES_PORT"),  # type: ignore[arg-type] # Pydantic-side validation
            DRIVER=get_str_from_env("POSTGRES_DRIVER"),
        )


class LoggingLevelSettings(BaseModel):
    logging_level: LoggingLevel = Field(alias="LOGGING_LEVEL")

    @classmethod
    def from_env(cls) -> "LoggingLevelSettings":
        return cls(
            LOGGING_LEVEL=get_str_from_env("LOGGING_LEVEL"),  # type: ignore[arg-type] # Pydantic-side validation
        )


class FernetKeySettings(BaseModel):
    fernet_key: str = Field(alias="FERNET_KEY_BASE64")

    @classmethod
    def from_env(cls) -> "FernetKeySettings":
        return cls(
            FERNET_KEY_BASE64=get_str_from_env("FERNET_KEY_BASE64"),
        )
