from domain.ports.api_key_encryption import APIKeyEncryption
from domain.ports.api_key_generator import APIKeyGenerator


class APIKeyService:
    def __init__(
        self, key_generator: APIKeyGenerator, key_encryption: APIKeyEncryption,
    ) -> None:
        pass
