from typing import List, Optional
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import delete, select
from src.reservations.domain.reservation import Reservation
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.infraestructure.mappers.restaurant_mapper import RestaurantMapper
from src.restaurants.infraestructure.model.menu_model import MenuModel
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.infraestructure.model.table_model import TableModel
from src.shared.utils.result import Result
from sqlalchemy.orm import selectinload


class RestaurantRepositoryImpl(IRestaurantRepository):

    def __init__(self, db: AsyncSession):
        super().__init__()
        self.db = db

    async def get_restaurant_by_id(self, restaurant_id: str) -> Optional[Restaurant]:
        try:
            statement = (
                select(RestaurantModel)
                .where(RestaurantModel.id == restaurant_id)
                .options(
                    selectinload(RestaurantModel.menu_items),
                    selectinload(RestaurantModel.tables)
                )
            )
            result = await self.db.exec(statement)  # ¡Usa execute, no exec!
            model = result.one_or_none()
            if model is None:
                return None
            return RestaurantMapper.to_domain(model)
        except Exception:
            # Si ocurre cualquier error inesperado, retorna None para evitar romper el flujo
            return None

    async def get_restaurant_by_name(self, name: str) -> List[Restaurant]:
        statement = select(RestaurantModel).where(RestaurantModel.name == name)
        results = await self.db.exec(statement)
        restaurants = results.all()
        return [RestaurantMapper.to_domain(r) for r in restaurants]

    async def get_all_restaurants(self) -> List[Restaurant]:
        statement = (
            select(RestaurantModel)
            .options(
                selectinload(RestaurantModel.menu_items),
                selectinload(RestaurantModel.tables)
            )
        )
        result = await self.db.exec(statement)
        restaurants_models: Optional[List[RestaurantModel]] = result.all()

        print("Lista de restaurants: ", restaurants_models)
        if restaurants_models is None:
            return []
        restaurants: List[Restaurant] = [RestaurantMapper.to_domain(r) for r in restaurants_models]
        return restaurants

    async def create_restaurant(self, restaurant: Restaurant) -> Result[Restaurant]:
        try:
            restaurant_model = RestaurantMapper.to_model(restaurant)
            self.db.add(restaurant_model)
            await self.db.commit()

            await self.db.refresh(restaurant_model, attribute_names=["menu_items", "tables"])

            return Result.success(RestaurantMapper.to_domain(restaurant_model))
        except Exception as e:
            await self.db.rollback()
            return Result.failure(error=e, messg=f"Error creating restaurant: {str(e)}")
        
    async def update_restaurant(self, restaurant: Restaurant) -> Restaurant:
        pass

    async def delete_restaurant_by_id(self, restaurant_id: UUID) -> Result[bool]:
        try:
            statement = select(RestaurantModel).where(RestaurantModel.id == restaurant_id)
            restaurant = (await self.db.exec(statement)).one_or_none()
            if not restaurant:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {restaurant_id} does not exist."
                )

            tables = (await self.db.exec(select(TableModel).where(TableModel.restaurant_id == restaurant_id))).all()
            if tables:
                return Result.failure(
                error=ValueError("The restaurant cannot be deleted because it has associated tables."),
                messg="The restaurant cannot be deleted because it has associated tables. Delete the tables first."
            )

            await self.db.delete(restaurant)
            await self.db.commit()
            return Result.success(True)
        except Exception as e:
            return Result.failure(error=e, messg="Error deleting restaurant")







