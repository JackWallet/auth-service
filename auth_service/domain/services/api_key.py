from domain.ports.api_key_encryption import APIKeyEncryption
from domain.ports.api_key_generator import APIKeyGenerator
from domain.ports.api_key_type import SecretKey


class APIKeyService:
    def __init__(
        self,
        key_generator: APIKeyGenerator[SecretKey],
        key_encryption: APIKeyEncryption[SecretKey],
    ) -> None:
        pass
