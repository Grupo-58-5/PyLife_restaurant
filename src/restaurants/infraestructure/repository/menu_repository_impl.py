from datetime import datetime
from typing import List
from uuid import UUID
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import exists, select
from sqlalchemy.orm import selectinload
from src.reservations.infraestructure.models.pre_order_model import PreOrder
from src.reservations.infraestructure.models.reservation_model import ReservationModel
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


    async def delete_or_disable_menu_item(self, menu_id: UUID) -> Result[bool]:
        try:
            # Busca una reserva futura que use ese plato
            check_statement = select(ReservationModel).join(PreOrder).where(
                PreOrder.dish_id == menu_id,
                ReservationModel.status != 'CANCELED'
            )
            reservation_model = (await self.db.exec(check_statement)).one_or_none()

            # Busca el plato (menu item)
            result_menu = await self.db.exec(select(MenuModel).where(MenuModel.id == menu_id))
            menu_item = result_menu.one_or_none()

            if not menu_item:
                return Result.failure(
                    error=ValueError(f"Menu item with id {menu_id} not found"),
                    messg=f"Menu item with id {menu_id} not found",
                    code=404
                )

            if reservation_model is not None:
                menu_item.available = False
                self.db.add(menu_item)
                await self.db.commit()
                return Result.success(True)
            else:
                await self.db.delete(menu_item)
                await self.db.commit()
                return Result.success(True)

        except Exception as e:
            print('Error aqui: ', e)
            return Result.failure(error=e, messg="Error deleting or disabling menu item")



        
