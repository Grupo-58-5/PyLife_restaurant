from uuid import UUID
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class DeleteRestaurantApplicationService(IApplicationService[UUID, Result[bool]]):

    def __init__(self, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.restaurant_repository = restaurant_repository

    async def execute(self, restaurant_id: UUID) -> Result[bool]:
        try:
            # 1. Buscar el restaurante
            restaurant = await self.restaurant_repository.get_restaurant_by_id(restaurant_id)
            if restaurant is None:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {restaurant_id} does not exist."
                )

            result = await self.restaurant_repository.delete_restaurant_by_id(restaurant_id)
            if result.is_error():
                return Result.failure(
                    code=404,
                    error=result.error,
                    messg=result.messg
                )
            return Result.success(True)
        except Exception as e:
            return Result.failure(Exception(str(e)), str(e), 500)