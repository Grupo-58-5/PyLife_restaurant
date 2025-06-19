


from typing import List
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class GetAllRestaurantApplicationService(IApplicationService[None, Result[List[BaseRestaurantResponse]]]):

    def __init__(self, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.repository = restaurant_repository

    async def execute( self ) -> Result[List[BaseRestaurantResponse]]:
        try:
            restaurants = await self.repository.get_all_restaurants()
            return Result[List[BaseRestaurantResponse]].success(
                [BaseRestaurantResponse(
                    id=r.get_id(), 
                    name=r.get_name(), 
                    address=r.get_address(), 
                    opening_hour=r.get_opening(), 
                    closing_hour=r.get_closing()) for r in restaurants]
            )
        except ValueError as ve:
            return Result[List[BaseRestaurantResponse]].failure(
                exception=ve, 
                message=str(ve), 
                status_code=400
            )
        except Exception as e:
            return Result[List[BaseRestaurantResponse]].failure(
                exception=e, 
                message=f"Error retrieving restaurants: {str(e)}", 
                status_code=500
            )