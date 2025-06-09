


from uuid import uuid4
from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.domain.vo.restaurant_address import RestaurantAddress
from src.restaurants.domain.vo.restaurant_name import RestaurantName
from src.restaurants.domain.vo.restaurant_schedule import RestaurantSchedule
from src.restaurants.infraestructure.model.menu_model import MenuModel
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel


class RestaurantMapper():

    @staticmethod
    def to_domain(restaurant_model: RestaurantModel) -> Restaurant:
        return Restaurant(
            id = restaurant_model.id,
            name = RestaurantName.create(restaurant_model.name),
            address = RestaurantAddress.create(restaurant_model.location),
            schedule = RestaurantSchedule.create(
                opening_time=restaurant_model.opening_time,
                closing_time=restaurant_model.closing_time
            ),
            menu = [MenuMapper.to_domain(item) for item in restaurant_model.menu_items] if restaurant_model.menu_items else []  
            
        ) 

    @staticmethod
    def to_model(data: Restaurant) -> RestaurantModel:
        return RestaurantModel(
            id = data.get_id(),
            name = data.get_name(),
            location = data.get_address(),
            opening_time = data.get_opening(),
            closing_time = data.get_closing(),
            menu_items = [MenuMapper.to_model(item) for item in data.get_menu()] if data.get_menu() else [],
        )    
    

class MenuMapper():

    @staticmethod
    def to_model(data: MenuEntity) -> MenuModel:
        return MenuModel(
            id=data.get_id(),
            name=data.name,
            description=data.description,
            category=data.category,
        )
    
    @staticmethod
    def to_domain(menu_model: MenuModel) -> MenuEntity:
        return MenuEntity.create(
            id=menu_model.id,
            name=menu_model.name,
            description=menu_model.description,
            category=menu_model.category
        )