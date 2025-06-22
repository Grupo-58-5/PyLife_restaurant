


from src.restaurants.domain.entity.table_entity import TableEntity
from uuid import uuid4
from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.domain.vo.restaurant_address import RestaurantAddress
from src.restaurants.domain.vo.restaurant_name import RestaurantName
from src.restaurants.domain.vo.restaurant_schedule import RestaurantSchedule
from src.restaurants.infraestructure.model.menu_model import MenuModel
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.infraestructure.model.table_model import TableModel


class RestaurantMapper():

    @staticmethod
    def to_domain(self, restaurant_model: RestaurantModel) -> Restaurant:
        return Restaurant(
            id = restaurant_model.id,
            name = RestaurantName.create(restaurant_model.name),
            address = RestaurantAddress.create(restaurant_model.location),
            schedule = RestaurantSchedule.create(
                opening_time=restaurant_model.opening_time,
                closing_time=restaurant_model.closing_time
            ),
            
        ) 

    @staticmethod
    def to_model(data: Restaurant) -> RestaurantModel:
        return RestaurantModel(
            id = data.get_id(),
            name = data.get_name(),
            location = data.get_address(),
            opening_time = data.get_opening(),
            closing_time = data.get_closing(),
            tables = []
        )    
    
    def table_to_domain(self, table_model: TableModel) -> TableEntity:
        """Convert a table model to a domain object."""
        return TableEntity(
            id=table_model.id,
            table_number=table_model.table_number,
            seats=table_model.capacity,
            location= table_model.location if table_model.location else None
        )
    
    def table_to_model(self, table: TableEntity) -> TableModel:
        """Convert a domain table object to a model."""
        return TableModel(
            id=table.get_id(),
            table_number=table.get_table_number(),
            capacity=table.get_seats(),
            location=table.get_location(),
            menu_items = [MenuMapper.to_model(item) for item in data.get_menu()] if data.get_menu() else [],
        )    
    

class MenuMapper():

    @staticmethod
    def to_model(data: MenuEntity) -> MenuModel:
        return MenuModel(
            id=uuid4(),
            name=data.get_name(),
            description=data.get_description(),
            category=data.get_category(),
        )
    
    @staticmethod
    def to_domain(menu_model: MenuModel) -> MenuEntity:
        return MenuEntity.create(
            id=menu_model.id,
            name=menu_model.name,
            description=menu_model.description,
            category=menu_model.category
        )