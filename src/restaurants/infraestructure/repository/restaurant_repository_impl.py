


from typing import Optional
from sqlmodel import Session, select
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.infraestructure.mappers.restaurant_mapper import RestaurantMapper
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel


class RestaurantRepositoryImpl(IRestaurantRepository):

    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    async def get_restaurant_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        statement = select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
        result = self.db.exec(statement)
        return result.first()

    async def get_all_restaurants(self) -> list[Restaurant]:
        statement = select(RestaurantModel)
        results = self.db.exec(statement)
        restaurants =  results.all()
        return [RestaurantMapper.to_domain(r) for r in restaurants]

    async def create_restaurant(self, restaurant: Restaurant) -> Restaurant:
        restaurant_model = RestaurantMapper.to_model(restaurant)
        self.db.add(restaurant_model)
        self.db.commit()
        self.db.refresh(restaurant_model)
        return restaurant

    async def update_restaurant(self, restaurant: Restaurant) -> Restaurant:
        pass

    async def delete_restaurant(self, restaurant_id: str) -> None:
        pass