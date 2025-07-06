from src.restaurants.application.schemas.entry.delete_menu_schema import DeleteMenuSchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItemBase, MenuItemResponse
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class DeleteMenuApplicationService(IApplicationService[DeleteMenuSchema, Result[bool]]):

    def __init__(self, restaurant_repo: IRestaurantRepository, menu_repo: IMenuRepository):
        self.restaurant_repo = restaurant_repo
        self.menu_repo = menu_repo

    async def execute(self, data: DeleteMenuSchema) -> Result[bool]:
        try:
            restaurant = await self.restaurant_repo.get_restaurant_by_id(data.restaurant_id)
            if not restaurant:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {data.restaurant_id} does not exist."
                )

            menu_restaurant = restaurant.get_menu()
            if not menu_restaurant or data.menu_id not in [item.get_id() for item in menu_restaurant]:
                return Result.failure(
                    error=ValueError("Menu item not found"),
                    messg=f"Menu with ID {data.menu_id} does not exist in the restaurant."
                )

            result = await self.menu_repo.delete_or_disable_menu_item(data.menu_id)
            if result.is_error():
                return Result.failure(
                    error=result.error,
                    messg=result.messg,
                    code=400
                )

            return Result.success(True)

        except Exception as e:
            return Result.failure(Exception(str(e)), str(e), 500)
