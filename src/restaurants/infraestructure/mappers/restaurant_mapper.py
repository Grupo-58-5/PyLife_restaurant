


from src.restaurants.domain.entity.table_entity import TableEntity
from src.restaurants.domain.restaurant import Restaurant
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.infraestructure.model.table_model import TableModel


class RestaurantMapper():

    @staticmethod
    def to_domain(self, restaurant_model: RestaurantModel) -> Restaurant:
        return Restaurant(
            id = restaurant_model.id,
            name = restaurant_model.name,
            address = restaurant_model.location,
            opening_hour = restaurant_model.opening_time,
            closing_hour = restaurant_model.closing_time,
            tables= [self.table_to_domian(t) for t in restaurant_model.tables] if restaurant_model.tables else []
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
            location=table.get_location()
        )