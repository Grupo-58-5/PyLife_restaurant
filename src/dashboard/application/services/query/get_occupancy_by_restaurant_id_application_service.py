

from datetime import datetime 
from uuid import UUID

from src.dashboard.application.schemas.response.occupancy_restaurant_response import OccupancyItemResponse
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class GetOccupancyByRestaurantIdApplicationService(IApplicationService[UUID, Result[OccupancyItemResponse]]):
    
    def __init__(self, restaurant_repository: RestaurantRepositoryImpl):
        self.restaurant_repository = restaurant_repository

    async def execute(self, restaurant_id: UUID) -> Result[OccupancyItemResponse]:
        try:
            restaurant = await self.restaurant_repository.get_restaurant_model(restaurant_id)
            if not restaurant:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg="No restaurant exists with that ID.",
                    code=404
                )
            
            today = datetime.now().date()
            tables = restaurant.tables
            total_tables = len(tables)
            reservation = restaurant.reservations
            occupied_tables = sum(1 for r in reservation if (today >= r.start_time.date() and today <= r.finish_time.date()))
            occupancy = (occupied_tables / total_tables) * 100 if total_tables > 0 else 0.0

            return Result.success(OccupancyItemResponse(
                restaurant_id=restaurant.id,
                restaurant_name=restaurant.name,
                occupancy=occupancy
            ))

        except Exception as e:
            return Result.failure(
                error=e,
                messg=f"Error calculating occupancy: {e}",
                code=500
            )