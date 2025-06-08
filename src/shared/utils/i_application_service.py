


from abc import ABC, abstractmethod
from typing import TypeVar, Generic

TService = TypeVar('TService')
TResponse = TypeVar('TResponse')


class IApplicationService(ABC, Generic[TService, TResponse]):
    """
    Interface for application services.
    """
    def __init__(self):
        super().__init__()

    @abstractmethod
    async def execute(self, data: TService) -> TResponse:
        pass