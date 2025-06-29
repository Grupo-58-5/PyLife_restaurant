# src/restaurants/application/services/update_menu_service.py

from uuid import UUID
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result
from src.restaurants.application.schemas.response.menu_item_response import MenuItemResponse, MenuItemBase
from src.restaurants.application.schemas.entry.create_menu_item_schema import UpdateMenuSchema
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository

class UpdateMenuApplicationService(
    IApplicationService[tuple[UUID, UUID, UpdateMenuSchema], Result[MenuItemResponse]]
):

    def __init__(self, menu_repo: IMenuRepository, restaurant_repo: IRestaurantRepository):
        super().__init__()
        self.menu_repo = menu_repo
        self.restaurant_repo = restaurant_repo

    async def execute(self, data: tuple[UUID, UUID, UpdateMenuSchema]) -> Result[MenuItemResponse]:
        try:
            restaurant_id, menu_id, menu_data = data

            restaurant = await self.restaurant_repo.get_restaurant_by_id(restaurant_id)
            if restaurant is None:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {restaurant_id} does not exist."
                )

            menus_in_restaurant = restaurant.get_menu()
            menu_target = next((menu for menu in menus_in_restaurant if menu.get_id() == menu_id), None)
            if menu_target is None:
                return Result.failure(
                    error=ValueError(f"Menu with ID {menu_id} not found in restaurant {restaurant_id}"),
                    messg=f"Menu with ID {menu_id} not found in restaurant {restaurant_id}."
                )

            # Actualizar solo campos provistos
            if menu_data.name is not None:
                menu_target.name = menu_data.name
            if menu_data.description is not None:
                menu_target.description = menu_data.description
            if menu_data.category is not None:
                menu_target.category = menu_data.category

            updated_menu_result = await self.menu_repo.update_item_menu(menu_id, menu_target)
            if updated_menu_result.is_error():
                return Result.failure(
                    error=updated_menu_result.error,
                    messg=f"Error updating menu: {updated_menu_result.error}"
                )

            updated_menu = updated_menu_result.result()

            return Result.success(
                MenuItemResponse(
                    restaurant_id=restaurant.id,  # o restaurant.get_id si no usas acceso directo
                    restaurant_name=restaurant.get_name(),
                    item=MenuItemBase(
                        id=updated_menu.get_id(),
                        name=updated_menu.get_name(),
                        description=updated_menu.get_description(),
                        category=updated_menu.get_category()
                    )
                )
            )

        except ValueError as ve:
            return Result.failure(error=ve, messg=str(ve))
        except Exception as e:
            return Result.failure(error=Exception(str(e)), messg=str(e))
