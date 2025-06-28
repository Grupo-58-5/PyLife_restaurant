


from typing import List
from uuid import UUID
from sqlmodel import Session, select
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

    def __init__(self, db : Session):
        super().__init__()
        self.db = db

    async def get_menu(self, restaurant_id: UUID) -> List[MenuEntity]:
        """
        Retrieves the menu for a specific restaurant.
        """
        statement = select(MenuModel).where(MenuModel.restaurant_id == restaurant_id)
        menu_model = self.db.exec(statement).all()
        if not menu_model:
            return []
        ## missing mapper
        return [MenuEntity(id=m.id, name=m.name, description=m.description, category=m.category) for m in menu_model]
    
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
            self.db.commit()
            self.db.refresh(menu_model)
            return Result.success(menu_data)
        except Exception as e:
            self.db.rollback()
            return Result.failure(
                error=e,
                messg=f"Error creating menu item: {str(e)}"
            )

    def update_item_menu(self, menu_id: UUID, menu_data: MenuEntity) -> MenuEntity:
        pass

    async def delete_item_menu(self, menu_id: UUID) -> Result[MenuEntity]:
        try:
            menu_model = self.db.get(MenuModel, menu_id)
            self.db.delete(menu_model)
            self.db.commit()
            return Result[MenuEntity].success(MenuMapper.to_domain(menu_model))
        except BaseException as e:
            print("Error: ",e)
            self.db.rollback()
            return Result[MenuEntity].failure(error=e,messg='DELETE failed')
        