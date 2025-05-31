

from abc import ABC, abstractmethod
from uuid import UUID

from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel

class IRestaurantRepository(ABC):

    @abstractmethod
    def get_all_restaurants(self) -> list[Restaurant]:
        pass

    @abstractmethod
    def get_restaurant_by_id(self, restaurant_id: UUID) -> Restaurant:
        pass

    @abstractmethod
    def create_restaurant(self, restaurant: CreateRestaurantSchema) -> Restaurant:
        pass

    @abstractmethod
    def update_restaurant(self, restaurant_id: UUID, restaurant: CreateRestaurantSchema) -> Restaurant:
        pass

    @abstractmethod
    def delete_restaurant(self, restaurant_id: UUID) -> None:
        pass
    


