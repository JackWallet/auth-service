from domain.entities.api_key import APIKeyAccessLevelEnum


def validate_api_key_access_level(
    input: APIKeyAccessLevelEnum, target: APIKeyAccessLevelEnum,
) -> None: ...
