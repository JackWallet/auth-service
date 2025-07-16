from pydantic import BaseModel, Field


class APIReaderKeySchema(BaseModel):
    api_key: str = Field(
        max_length=256,
        min_length=256,
        description="Only 256 characters are allowed for the api key",
        alias="X-AUTH_READER_API_KEY",
    )


class APIWriterKeySchema(BaseModel):
    api_key: str = Field(
        max_length=256,
        min_length=256,
        description="Only 256 characters are allowed for the api key",
        alias="X-AUTH_WRITER_API_KEY",
    )
