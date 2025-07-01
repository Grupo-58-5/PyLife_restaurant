from uuid import UUID
from src.restaurants.application.schemas.entry.resaurant_schema_entry import UpdateRestaurantSchema
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.vo.restaurant_address import RestaurantAddress
from src.restaurants.domain.vo.restaurant_name import RestaurantName
from src.restaurants.domain.vo.restaurant_schedule import RestaurantSchedule
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class UpdateRestaurantApplicationService(IApplicationService[tuple[UUID, UpdateRestaurantSchema], Result[BaseRestaurantResponse]]):

    def __init__(self, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.restaurant_repository = restaurant_repository

    async def execute(self, data: tuple[UUID, UpdateRestaurantSchema]) -> Result[BaseRestaurantResponse]:
        try:
            restaurant_id, update_data = data

            # Obtener restaurante actual
            restaurant = await self.restaurant_repository.get_restaurant_by_id(restaurant_id)
            if restaurant is None:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {restaurant_id} does not exist."
                )

            # Aplicar actualizaciones condicionales
            if update_data.name is not None:
                restaurant.name = RestaurantName(update_data.name)
            if update_data.address is not None:
                restaurant.address = RestaurantAddress(update_data.address)
            if update_data.opening_time is not None and update_data.closing_time is not None:
                restaurant.schedule = RestaurantSchedule(opening_time=update_data.opening_time, closing_time=update_data.closing_time)

            result = await self.restaurant_repository.update_restaurant(restaurant)
            if result.is_error():
                return Result.failure(
                    error=result.error,
                    messg=f"Error updating restaurant: {str(result.error) if result.error else 'Unknown error'}"
                )
            
            updated = result.result()
            return Result.success(BaseRestaurantResponse(
                print("-----TYPT: ", type(updated)),
                id=updated.get_id(),
                name=updated.get_name(),
                location=updated.get_address(),
                opening_time=updated.get_opening(),
                closing_time=updated.get_closing(),
            ))

        except ValueError as ve:
            return Result.failure(error=ve, messg=str(ve), code=400)
        except Exception as e:
            return Result.failure(error=Exception(str(e)), messg=str(e), code=500)