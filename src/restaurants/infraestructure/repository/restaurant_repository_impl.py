


from typing import List, Optional
from sqlmodel import Session, select
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.infraestructure.mappers.restaurant_mapper import RestaurantMapper
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.shared.utils.result import Result
from sqlalchemy.orm import selectinload


class RestaurantRepositoryImpl(IRestaurantRepository):

    def __init__(self, db: Session):
        super().__init__()
        self.db = db

    async def get_restaurant_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        statement =  statement = (
            select(RestaurantModel)
            .where(RestaurantModel.id == restaurant_id)
            .options(selectinload(RestaurantModel.menu_items))
        )
        result = self.db.exec(statement)
        return RestaurantMapper.to_domain(result.one_or_none()) if result else None
    
    async def get_restaurant_by_name(self, name: str) -> List[Restaurant]:
        statement = select(RestaurantModel).where(RestaurantModel.name == name)
        results = self.db.exec(statement)
        restaurants = results.all()
        return [RestaurantMapper.to_domain(r) for r in restaurants]

    async def get_all_restaurants(self) -> List[Restaurant]:
        statement = select(RestaurantModel)
        results = self.db.exec(statement)
        restaurants =  results.all()
        return [RestaurantMapper.to_domain(r) for r in restaurants]

    async def create_restaurant(self, restaurant: Restaurant) -> Result[Restaurant]:
        try:
            restaurant_model = RestaurantMapper.to_model(restaurant)
            self.db.add(restaurant_model)
            self.db.commit()
            self.db.refresh(restaurant_model)
            _ = restaurant_model.menu_items  # Load menu items if any
            return Result.success(RestaurantMapper.to_domain(restaurant_model))
        except Exception as e:
            self.db.rollback()
            return Result.failure(error=e, messg=f"Error creating restaurant: {str(e)}")

    async def update_restaurant(self, restaurant: Restaurant) -> Restaurant:
        pass

    async def delete_restaurant(self, restaurant_id: str) -> None:
        pass