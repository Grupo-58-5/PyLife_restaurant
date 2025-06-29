from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.restaurants.domain.entity.table_entity import TableEntity
from src.restaurants.domain.restaurant import Restaurant
from src.shared.utils.result import Result


class ITableRepository(ABC):
    """
    Interface for table repository.
    """

    @abstractmethod
    async def get_table(self, restaurant_id: UUID) -> List[TableEntity]:
        pass

    @abstractmethod
    async def get_table_by_id(self, table_id: UUID) -> Result[TableEntity]:
        pass

    @abstractmethod
    async def create_item_table(self, table_data: TableEntity , restaurant_id: UUID) -> Result[TableEntity]:
        pass

    @abstractmethod
    async def update_item_table(self, table_id: UUID, table_data: TableEntity) -> Result[TableEntity]:
        pass

    @abstractmethod
    async def delete_item_table_or_disable(self, table_id: UUID) -> Result[None]:
        pass