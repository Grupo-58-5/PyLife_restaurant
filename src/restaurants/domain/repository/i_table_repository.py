from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.restaurants.domain.entity.table_entity import TableEntity
from src.shared.utils.result import Result


class ITableRepository(ABC):
    """
    Interface for table repository.
    """

    @abstractmethod
    async def get_table(self, restaurant_id: UUID) -> List[TableEntity]:
        pass

    @abstractmethod
    async def create_item_table(self, table_data: TableEntity , restaurant_id: UUID) -> Result[TableEntity]:
        pass
        
    @abstractmethod    
    def update_item_table(self, table_id: UUID, table_data: TableEntity) -> TableEntity:
        pass

    @abstractmethod    
    def delete_item_table(self, table_id: UUID) -> None:
        pass