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
from src.restaurants.infraestructure.model.table_model import TableModel


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
                    selectinload(RestaurantModel.tables.and_(TableModel.is_active == True))
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
        
    async def update_restaurant(self, restaurant: Restaurant) -> Result[Restaurant]:
        try:
            restaurant_model = await self.get_restaurant_model(restaurant.get_id())
            if not restaurant_model:
                return Result.failure(
                    error=ValueError(f"Restaurant with id {restaurant.get_id()} not found"),
                    messg=f"Restaurant with id {restaurant.get_id()} not found"
                )

            restaurant_model.name = restaurant.get_name()
            restaurant_model.location = restaurant.get_address()
            restaurant_model.opening_time = restaurant.get_opening()
            restaurant_model.closing_time = restaurant.get_closing()

            print('Este es el restaurant a guardar:', restaurant_model)

            self.db.add(restaurant_model)
            await self.db.commit()
            await self.db.refresh(restaurant_model)

            return Result.success(RestaurantMapper.to_model(restaurant_model))
        except Exception as e:
            return Result.failure(error=e, messg=f"Error updating restaurant: {str(e)}")


    async def delete_restaurant_by_id(self, restaurant_id: UUID) -> Result[bool]:
        try:
            restaurant = await self.get_restaurant_model(restaurant_id)
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
        
    async def get_restaurant_model(self, id: UUID) -> Optional[RestaurantModel]:
        statement = (
                select(RestaurantModel)
                .where(RestaurantModel.id == id)
                .options(
                    selectinload(RestaurantModel.menu_items),
                    selectinload(RestaurantModel.tables.and_(TableModel.is_active == True))
                )
            )
        return (await self.db.exec(statement)).one_or_none()







