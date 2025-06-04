


from uuid import uuid4
from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema
from src.restaurants.application.schemas.response.restaurant_schema_response import RestaurantDetailResponse
from src.restaurants.domain.entity.table_entity import TableEntity
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.restaurant import Restaurant
from src.shared.utils.i_application_service import IApplicationService


class CreateRestaurantApplicationService(IApplicationService[CreateRestaurantSchema, RestaurantDetailResponse]):
    def __init__(self, restaurant_repository: IRestaurantRepository):
        self.repository = restaurant_repository

    async def execute(self, data: CreateRestaurantSchema) -> RestaurantDetailResponse:
        try:
            restaurant_id = uuid4()

            restaurant = Restaurant(
                id=restaurant_id,
                name=data.name,
                address=data.address,
                opening_hour=data.opening_hour,
                closing_hour=data.closing_hour,
                tables=[]
            )
            saved_restaurant = await self.repository.create_restaurant(restaurant)

            return RestaurantDetailResponse(
                id=restaurant.get_id(),
                name=restaurant.get_name(),
                address=restaurant.get_address(),
                opening_hour=restaurant.get_opening(),
                closing_hour=restaurant.get_closing(),
                tables = []
                )
        except Exception as e:
            raise Exception(f"Error creating restaurant: {str(e)}") from e