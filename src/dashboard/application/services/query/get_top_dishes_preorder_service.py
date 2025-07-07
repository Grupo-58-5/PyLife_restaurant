from typing import List
from src.dashboard.application.schemas.entry.get_top_dishes_entry_schema import GetTopDishesEntrySchema
from src.dashboard.application.schemas.response.top_dishes_response_schema import TopDishesResponseSchema
from src.reservations.domain.repository.reservation_repository import IReservationRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class GetTopDishesPreorderService(IApplicationService[GetTopDishesEntrySchema, Result[List[TopDishesResponseSchema]]]):

    def __init__(self, repo_reservation: IReservationRepository, repo_restaurant: IRestaurantRepository):
        super().__init__()
        self.repo_reservation = repo_reservation
        self.repo_restaurant = repo_restaurant
    
    async def execute(self, data: GetTopDishesEntrySchema) -> Result[List[TopDishesResponseSchema]]:
        try:
            # Verificar que el restaurante exista
            restaurant = await self.repo_restaurant.get_restaurant_by_id(data.restaurant_id)
            if not restaurant:
                return Result.failure(
                    ValueError("Restaurant not found"),
                    f"Restaurant with ID {data.restaurant_id} does not exist.",
                    404
                )

            # Obtener top platos preordenados
            result = await self.repo_reservation.get_top_dishes(
                restaurant_id=data.restaurant_id,
                start_date=data.start_date,
                end_date=data.end_date
            )

            if result.is_error():
                return Result.failure(
                    result.error,
                    f"Error retrieving top dishes: {result.get_error_message()}",
                    result.get_error_code()
                )

            return result
        except Exception as e:
            print(f"Error in GetTopDishesPreorderService: {e}")
            return Result.failure(e,"Unexpected error getting top dishes",500)




