

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from src.restaurants.domain.restaurant import Restaurant
from src.shared.utils.result import Result

class IRestaurantRepository(ABC):

    @abstractmethod
    async def get_all_restaurants(self) -> List[Restaurant]:
        pass

    @abstractmethod
    async def get_restaurant_by_name(self, name: str) -> List[Restaurant]:
        """Retrieve restaurants by name."""
        pass

    @abstractmethod
    async def get_restaurant_by_id(self, restaurant_id: UUID) -> Optional[Restaurant]:
        pass

    @abstractmethod
    async def create_restaurant(self, restaurant: Restaurant) -> Result[Restaurant]:
        pass

    @abstractmethod
    def update_restaurant(self, restaurant_id: UUID, restaurant: Restaurant) -> Result[Restaurant]:
        pass

    @abstractmethod
    def delete_restaurant_by_id(self, restaurant_id: UUID) -> Result[None]:
        pass

    # @abstractmethod
    # def delete_table_by_restaurant_id(self, restaurant_id: UUID) -> None:
    #     pass

    # @abstractmethod
    # def create_table_by_restaurant_id(self, restaurant_id: UUID, table: TableRestaurantSchema) -> None:
    #     pass
    


