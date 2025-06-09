

from typing import List
from uuid import UUID

from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.vo.restaurant_address import RestaurantAddress
from src.restaurants.domain.vo.restaurant_name import RestaurantName
from src.restaurants.domain.vo.restaurant_schedule import RestaurantSchedule


class Restaurant:
    def __init__(self, id: UUID, name: RestaurantName, address: RestaurantAddress, schedule: RestaurantSchedule, menu: List[MenuEntity] = []):
        self.validate()
        if not isinstance(id, UUID):
            raise ValueError("id must be an instance of UUID")
        """Initializes a Restaurant instance."""
        self.id = id
        self.name = name
        self.address = address
        self.schedule = schedule
        self.menu = menu

    def __repr__(self):
        return f"Restaurant(id={self.id}, name={self.name}, address={self.address})"
    
    def __eq__(self, other):
        if not isinstance(other, Restaurant):
            return False
        return self.id == other.id
    
    @classmethod
    def create(cls, id: UUID, name: RestaurantName, address: RestaurantAddress, schedule: RestaurantSchedule, menu: List[MenuEntity] = []) -> "Restaurant":
        """Factory method to create a Restaurant instance."""
        return cls(id, name, address, schedule, menu)
    
    def validate(self) -> None:
        """Validates the restaurant."""
        if not isinstance(self.name, RestaurantName):
            raise ValueError("name must be an instance of RestaurantName")
        if not isinstance(self.address, RestaurantAddress):
            raise ValueError("address must be an instance of RestaurantAddress")
        if not isinstance(self.schedule, RestaurantSchedule):
            raise ValueError("schedule must be an instance of RestaurantSchedule")
        for item in self.menu:
            if not isinstance(item, MenuEntity):
                raise ValueError("All menu items must be instances of MenuEntity")
    
    @name.setter
    def name(self, value: RestaurantName) -> None:
        """Sets the name of the restaurant."""
        if not isinstance(value, RestaurantName):
            raise ValueError("name must be an instance of RestaurantName")
        self.name = value
    
    @address.setter
    def address(self, value: RestaurantAddress) -> None:
        """Sets the address of the restaurant."""
        if not isinstance(value, RestaurantAddress):
            raise ValueError("address must be an instance of RestaurantAddress")
        self.address = value

    @schedule.setter
    def schedule(self, value: RestaurantSchedule) -> None:
        """Sets the schedule of the restaurant."""
        if not isinstance(value, RestaurantSchedule):
            raise ValueError("schedule must be an instance of RestaurantSchedule")
        self.schedule = value
    
    def get_id(self) -> UUID:
        return self.id
    
    def get_name(self) -> str:
        return self.name.name
    
    def get_address(self) -> str:
        return self.address.address
    
    def get_opening(self) -> str:
        return self.schedule.opening_time
    
    def get_closing(self) -> str:
        return self.schedule.closing_time
    
    def get_menu(self) -> List[MenuEntity]:
        return self.menu
    
    def add_menu_item(self, menu_item: MenuEntity) -> None:
        """Adds a menu item to the restaurant's menu."""
        if not isinstance(menu_item, MenuEntity):
            raise ValueError("menu_item must be an instance of MenuEntity")
        if len(self.menu) > 0:
            # Check if a menu item with the same name already exists
            # in the restaurant's menu
            if menu_item in self.menu:
                raise ValueError("Menu item already exists in the restaurant's menu")
            
            for item in self.menu:
                if item.name() == menu_item.name():
                    raise ValueError("Menu item with the same name already exists in the restaurant's menu")
    
        self.menu.append(menu_item)
