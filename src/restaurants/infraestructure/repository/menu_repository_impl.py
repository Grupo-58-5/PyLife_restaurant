from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from sqlalchemy.orm import selectinload
from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.infraestructure.mappers.restaurant_mapper import MenuMapper
from src.restaurants.infraestructure.model.menu_model import MenuModel
from src.shared.utils.result import Result


class MenuRepositoryImpl(IMenuRepository):

    """
    Implementation of the IMenuRepository interface.
    This class is responsible for managing the menu data.
    """

    def __init__(self, db : AsyncSession):
        super().__init__()
        self.db = db

    async def create_item_menu(self, menu_data: MenuEntity, restaurant_id: UUID) -> MenuEntity:
        """
        Creates a new menu item for a restaurant.
        """
        try:
            menu_model = MenuModel(
                id=menu_data.get_id(),
                name=menu_data.get_name(),
                description=menu_data.get_description(),
                category=menu_data.get_category(),
                available=True,
                restaurant_id=restaurant_id
            )
            self.db.add(menu_model)
            await self.db.commit()
            await self.db.refresh(menu_model)
            return Result.success(menu_data)
        except Exception as e:
            await self.db.rollback()
            return Result.failure(
                error=e,
                messg=f"Error creating menu item: {str(e)}"
            )

    async def update_item_menu(self, menu_id: UUID, menu_data: MenuEntity) -> Result[MenuEntity]:
        try:
            statement = select(MenuModel).where(MenuModel.id == menu_id)
            menu_model = (await self.db.exec(statement)).one_or_none()
            if not menu_model:
                return Result.failure(
                    error=ValueError(f"Menu item with id {menu_id} not found"),
                    messg=f"Menu item with id {menu_id} not found"
                )
            
            # Actualizar campos del modelo con los datos de la entidad
            menu_model.name = menu_data.get_name()
            menu_model.description = menu_data.get_description()
            menu_model.category = menu_data.get_category()
            # Si tienes el campo available:
            if hasattr(menu_data, "get_available"):
                menu_model.available = menu_data.get_available()

            self.db.add(menu_model)
            await self.db.commit()
            await self.db.refresh(menu_model)

            return Result.success(MenuMapper.to_domain(menu_model))
        except Exception as e:
            await self.db.rollback()
            return Result.failure(error=e, messg="Error updating menu item")


    async def delete_item_menu(self, menu_id: UUID) -> Result[MenuEntity]:
        try:
            menu_model = await self.db.get(MenuModel, menu_id)
            if menu_model is None:
                return Result.failure(
                    error=ValueError("Menu item not found"),
                    messg="Menu item does not exist"
                )
            
            self.db.delete(menu_model)
            await self.db.commit()
            
            return Result.success(MenuMapper.to_domain(menu_model))
        except Exception as e:
            print("Error deleting menu item:", e)
            await self.db.rollback()
            return Result.failure(error=e, messg='DELETE failed')

        
