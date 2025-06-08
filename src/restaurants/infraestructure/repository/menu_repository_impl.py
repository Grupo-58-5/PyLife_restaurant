


from typing import List
from uuid import UUID
from sqlmodel import Session, select
from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.infraestructure.model.menu_model import MenuModel


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
        menu_model = MenuModel(
            id=menu_data.id,
            name=menu_data.name,
            description=menu_data.description,
            category=menu_data.category,
            available=True,
            restaurant_id=restaurant_id
        )
        self.db.add(menu_model)
        self.db.commit()
        self.db.refresh(menu_model)
        return menu_data


    def update_item_menu(self, menu_id: UUID, menu_data: MenuEntity) -> MenuEntity:
        pass

    def delete_item_menu(self, menu_id: UUID) -> None:
        pass