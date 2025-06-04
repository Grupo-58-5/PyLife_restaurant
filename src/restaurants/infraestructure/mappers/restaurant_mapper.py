


from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel


class RestaurantMapper():

    @staticmethod
    def to_domain(restaurant_model: RestaurantModel) -> Restaurant:
        return Restaurant(
            id = restaurant_model.id,
            name = restaurant_model.name,
            address = restaurant_model.location,
            opening_hour = restaurant_model.opening_time,
            closing_hour = restaurant_model.closing_time,
            tables=[]
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