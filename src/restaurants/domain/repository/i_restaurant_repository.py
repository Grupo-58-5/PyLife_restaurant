

from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema
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
    async def get_restaurant_by_id(self, restaurant_id: UUID) -> Restaurant:
        pass

    @abstractmethod
    async def create_restaurant(self, restaurant: Restaurant) -> Result[Restaurant]:
        pass

    @abstractmethod
    def update_restaurant(self, restaurant_id: UUID, restaurant: Restaurant) -> Restaurant:
        pass

    @abstractmethod
    def delete_restaurant(self, restaurant_id: UUID) -> None:
        pass
    


