

from typing import List
from uuid import UUID

from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.entity.table_entity import TableEntity
from src.restaurants.domain.vo.restaurant_address import RestaurantAddress
from src.restaurants.domain.vo.restaurant_name import RestaurantName
from src.restaurants.domain.vo.restaurant_schedule import RestaurantSchedule


class Restaurant:
    def __init__(self, id: UUID, name: RestaurantName, address: RestaurantAddress, schedule: RestaurantSchedule, menu: List[MenuEntity] | None = None, tables: List[TableEntity] | None = None):
        self.id = id
        self.name = name
        self.address = address
        self.schedule = schedule
        self.menu = menu if menu is not None else []
        self.tables = tables if tables is not None else []


    def __repr__(self):
        return f"Restaurant(id={self.id}, name={self.name.get_name()}, address={self.address.get_address()})"
    
    def __eq__(self, other):
        if not isinstance(other, Restaurant):
            return False
        return self.id == other.id
    
    @classmethod
    def create(cls, id: UUID, name: RestaurantName, address: RestaurantAddress, schedule: RestaurantSchedule, menu: List[MenuEntity] | None = None, tables: List[TableEntity] | None = None) -> "Restaurant":

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
    
    def get_tables(self) -> List[TableEntity]:
        return self.tables
    
    def add_menu_item(self, menu_item: MenuEntity) -> None:
        """Adds a menu item to the restaurant's menu."""
        if not isinstance(menu_item, MenuEntity):
            raise ValueError("menu_item must be an instance of MenuEntity")
        if self.menu and len(self.menu) > 0:
            # Check if a menu item with the same name already exists
            # in the restaurant's menu
            new_name = menu_item.get_name().strip().lower()
            existing_names = [item.get_name().strip().lower() for item in self.menu]
            if new_name in existing_names:
                raise ValueError("Menu item with the same name already exists in the restaurant's menu")
            
        if self.menu is None:
            self.menu = []
        self.menu.append(menu_item)

    def add_menu_items_bulk(self, menu_items: List[MenuEntity]) -> None:
        """Adds a list of menu items to the restaurant, validating duplicates after building the list."""
        existing_names = {item.get_name().strip().lower() for item in self.menu}
        new_names = set()

        for item in menu_items:
            name_clean = item.get_name().strip().lower()
            if name_clean in existing_names or name_clean in new_names:
                raise ValueError(f"Duplicate menu item name found: '{item.get_name()}'")
            new_names.add(name_clean)

        self.menu.extend(menu_items)

    def add_table(self, table: TableEntity) -> None:
        """Adds a table to the restaurant."""
        if not isinstance(table, TableEntity):
            raise ValueError("table must be an instance of TableEntity")
        if self.tables and len(self.tables) > 0:
            # Check if a table with the same number already exists
            new_number = table.get_table_number()
            existing_numbers = [t.get_table_number() for t in self.tables]
            if new_number in existing_numbers:
                raise ValueError(f"Table with number {new_number} already exists in the restaurant")
            
        if self.tables is None:
            self.tables = []
        self.tables.append(table)
    
    def add_tables_bulk(self, tables: List[TableEntity]) -> None:
        """Adds a list of tables to the restaurant, validating duplicates after building the list."""
        existing_numbers = {table.get_table_number() for table in self.tables}
        new_numbers = set()

        for table in tables:
            table_number = table.get_table_number()
            if table_number in existing_numbers or table_number in new_numbers:
                raise ValueError(f"Duplicate table number found: {table_number}")
            new_numbers.add(table_number)

        self.tables.extend(tables)