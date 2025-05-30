


from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService


class GetAllRestaurantApplicationService(IApplicationService[None, list[BaseRestaurantResponse]]):
    def __init__(self, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.repository = restaurant_repository

    async def execute( self ) -> list[BaseRestaurantResponse]:
        try:
            restaurants = await self.restaurant_repository.get_all_restaurants()
            return [BaseRestaurantResponse(id=r.get_id(), name=r.get_name(), address=r.get_address(), opening_hour=r.get_opening(), closing_hour=r.get_closing()) for r in restaurants]
        except Exception as e:
            raise Exception(f"Error retrieving restaurants: {str(e)}") from e