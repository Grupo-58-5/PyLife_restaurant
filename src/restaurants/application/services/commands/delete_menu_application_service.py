




from src.restaurants.application.schemas.entry.delete_menu_schema import DeleteMenuSchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItemBase, MenuItemResponse
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class DeleteMenuApplicationService(IApplicationService[DeleteMenuSchema, Result[MenuItemResponse]]):

    def __init__(self, restaurant_repo: IRestaurantRepository, menu_repo: IMenuRepository):
        self.restaurant_repo = restaurant_repo
        self.menu_repo = menu_repo



    async def execute(self, data: DeleteMenuSchema) -> Result[MenuItemResponse]:
        try:

            restaurant = await self.restaurant_repo.get_restaurant_by_id(data.restaurant_id)
            if not restaurant:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {data.restaurant_id} does not exist."
                )
            
            menu_restaurant = restaurant.get_menu()
            if menu_restaurant and len(menu_restaurant) > 0:
                existing_ids = [item.get_id() for item in menu_restaurant]
                if data.menu_id not in existing_ids:
                    return Result.failure(
                        error =ValueError("Menu item with the same name already exists in the restaurant's menu"),
                        messg=f"Menu with ID {data.menu_id} does not exist."
                        )
            
            
            # menu_item = self.menu_repo.get_menu_item_by_id(data.menu_id, data.restaurant_id)
            # if not menu_item:
            #     return Result.failure(
            #         error=ValueError("Menu item not found"),
            #         messg=f"Menu item with ID {data.menu_id} does not exist in restaurant {data.restaurant_id}."
            #     )
            
            deleted_item = await self.menu_repo.delete_item_menu(data.menu_id)
            if deleted_item.is_error():
                return Result.failure(
                    error=deleted_item.error,
                    messg=deleted_item.messg
                )
            
            deleted_item = deleted_item.result()
            return Result.success(
                MenuItemResponse(
                    restaurant_id=restaurant.get_id(),
                    restaurant_name=restaurant.get_name(),
                    item=MenuItemBase(
                        id=deleted_item.get_id(),
                        name=deleted_item.get_name(),
                        description=deleted_item.get_description(),
                        category=deleted_item.get_category()
                    )
                )
            )
        

        except Exception as e:
            return Result.failure(Exception(str(e)), str(e), 500)    
