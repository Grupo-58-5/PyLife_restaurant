

from abc import ABC, abstractmethod
from uuid import UUID

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
    def create_restaurant(self, restaurant: Restaurant) -> Restaurant:
        pass

    @abstractmethod
    def update_restaurant(self, restaurant_id: UUID, restaurant: Restaurant) -> Restaurant:
        pass

    @abstractmethod
    def delete_restaurant(self, restaurant_id: UUID) -> None:
        pass

    # @abstractmethod
    # def delete_table_by_restaurant_id(self, restaurant_id: UUID) -> None:
    #     pass

    # @abstractmethod
    # def create_table_by_restaurant_id(self, restaurant_id: UUID, table: TableRestaurantSchema) -> None:
    #     pass
    


