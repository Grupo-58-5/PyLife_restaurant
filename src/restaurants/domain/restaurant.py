

from typing import List, Optional
from uuid import UUID

from src.restaurants.domain.entity.menu_entity import MenuEntity


class Restaurant:
    def __init__(self, id: UUID, name: str, address: str, opening_hour: str, closing_hour: str, menu: Optional[List[MenuEntity]] = None):
        self.id = id
        self.name = name
        self.address = address
        self.opening_hour = opening_hour
        self.closing_hour = closing_hour
        self.menu = menu

    def __repr__(self):
        return f"Restaurant(id={self.id}, name={self.name}, address={self.address}, opening_hour={self.opening_hour}, closing_hour={self.closing_hour})"
    
    def get_id(self) -> UUID:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_address(self) -> str:
        return self.address
    
    def get_opening(self) -> str:
        return self.opening_hour
    
    def get_closing(self) -> str:
        return self.closing_hour
