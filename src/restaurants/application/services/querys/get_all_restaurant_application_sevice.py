


from typing import List
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class GetAllRestaurantApplicationService(IApplicationService[None, Result[list[BaseRestaurantResponse]]]):

    def __init__(self, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.repository = restaurant_repository

    async def execute(self) -> Result[list[BaseRestaurantResponse]]:
        try:
            restaurant = await self.repository.get_all_restaurants()
            response = Result[list[BaseRestaurantResponse]].success(
                [BaseRestaurantResponse(id=r.get_id(), name=r.get_name(), address=r.get_address(), opening_hour=r.get_opening(), closing_hour=r.get_closing()) for r in restaurant]
            )
            return response
        except Exception as e:
            print(f"Error retrieving restaurants: {str(e)}")
            return Result[list[BaseRestaurantResponse]].failure(
                error=e,
                code=500,
                messg="Error retrieving restaurants: " + str(e)
            )
