


from src.restaurants.application.schemas.response.restaurant_schema_response import RestaurantDetailResponse
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class GetRestaurantApplicationService(IApplicationService[str, Result[RestaurantDetailResponse]]):	
    """
    Service to get a restaurant by its ID.
    """

    def __init__(self, restaurant_repository: IRestaurantRepository):
        self.repo = restaurant_repository

    async def execute(self, restaurant_id: str) -> Result[RestaurantDetailResponse]:
        """
        Get a restaurant by its ID.
        """
        try:
            restaurant = await self.repo.get_restaurant_by_id(restaurant_id)
            if not restaurant:
                return Result.failure(
                    Exception("Restaurant not found with id: " + restaurant_id),
                    "Restaurant not found",
                    404
                )
            return Result.success(
                RestaurantDetailResponse(
                    id=restaurant.get_id(),
                    name=restaurant.get_name(),
                    address=restaurant.get_address(),
                    opening_hour=restaurant.get_opening(),
                    closing_hour=restaurant.get_closing(),
                    menu_items=[{
                        "id": item.get_id(),
                        "name": item.get_name(),
                        "description": item.get_description(),
                        "category": item.get_category()
                    } for item in restaurant.get_menu()]
                    # tables=[{
                    #     "id": table.get_id(),
                    #     "capacity": table.get_capacity(),
                    #     "location": table.get_location()
                    # } for table in restaurant.get_tables()]
                )
            )
        except ValueError as ve:
            return Result.failure(
                ve,
                str(ve),
                400
            )
        except Exception as e:
            print(e)
            return Result.failure(
                e,
                f"Error retrieving restaurant: {str(e)}",
                500
            )