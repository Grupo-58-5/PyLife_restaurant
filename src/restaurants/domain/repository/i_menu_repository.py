from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.shared.utils.result import Result


class IMenuRepository(ABC):
    """
    Interface for menu repository.
    """

    @abstractmethod
    async def create_item_menu(self, menu_data: MenuEntity , restaurant_id: UUID) -> Result[MenuEntity]:
        pass

    @abstractmethod
    def update_item_menu(self, menu_id: UUID, menu_data: MenuEntity) -> MenuEntity:
        pass

    @abstractmethod
    def delete_item_menu(self, menu_id: UUID) -> None:
        pass