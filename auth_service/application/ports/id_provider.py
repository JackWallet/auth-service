from abc import ABC, abstractmethod


class IdProvider(ABC):
    @abstractmethod
    async def get_user_acknowledgements(
        self, data: dict[str, str],
    ) -> dict[str, str]:
        raise NotImplementedError
