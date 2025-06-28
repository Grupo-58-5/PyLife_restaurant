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

    async def get_menu(self, restaurant_id: UUID) -> List[MenuEntity]:
        """
        Retrieves the menu for a specific restaurant.
        """
        statement = select(MenuModel).where(MenuModel.restaurant_id == restaurant_id)
        menu_model = (await self.db.exec(statement)).all()
        if not menu_model:
            return []
        ## missing mapper
        return [MenuMapper.to_domain(m) for m in menu_model]

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

    def update_item_menu(self, menu_id: UUID, menu_data: MenuEntity) -> MenuEntity:
        pass

    def delete_item_menu(self, menu_id: UUID) -> None:
        pass

    async def get_menu_resturant(self, menu_id: UUID, restaurant_id: UUID) -> Result[MenuEntity]:
        """
        Verify that a menu belong to a specific restaurant and get the menu.
        """
        try:
            statement = (
                select(MenuModel)
                .where(
                    MenuModel.id == menu_id,
                    MenuModel.restaurant_id == restaurant_id
                )
                .options(
                    selectinload(MenuModel.restaurant),
                )
            )
            result = (await self.db.exec(statement)).one_or_none()
            if result is None:
                return Result[MenuEntity].failure(Exception,f'Dish #{menu_id} does not belong to the restaurant menu)',400)
            return Result.success(MenuMapper.to_domain(result))
        except Exception as e:
            return Result.failure(
                error=e,
                messg=f"Error searching for menu: {str(e)}"
            )
