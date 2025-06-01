from typing import NewType, cast

from pydantic import BaseModel, Field, PostgresDsn, field_validator

PostgresSettingsDsn = NewType("PostgresSettingsDsn", str)


class PostgresSettings(BaseModel):
    user: str = Field(alias="USER")
    password: str = Field(alias="PASSWORD")
    db: str = Field(alias="DB")
    host: str = Field(alias="HOST")
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
                    host=self.host,
                    port=self.port,
                    path=self.db,
                ),
            ),
        )
