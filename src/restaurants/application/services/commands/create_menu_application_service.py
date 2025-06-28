from uuid import uuid4
from src.restaurants.application.schemas.entry.create_menu_item_schema import CreateMenuItemSchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItem, MenuItemBase, MenuItemResponse
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class CreateMenuItemApplicationService(IApplicationService[CreateMenuItemSchema, Result[MenuItemResponse]]):
    """
    Service class responsible for handling the creation of menu items within a restaurant context.
    """
    def __init__(self, menu_repository: IMenuRepository, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.menu_repository = menu_repository
        self.restaurant_repository = restaurant_repository

    async def execute(self, data: CreateMenuItemSchema) -> Result[MenuItemResponse]:
        try:
            restaurant = await self.restaurant_repository.get_restaurant_by_id(data.restaurant_id)
            if not restaurant:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {data.restaurant_id} does not exist."
                )
            
            item = MenuEntity.create(
                id= uuid4(),
                name=data.name,
                description=data.description,
                category=data.category
            )
            
            restaurant.add_menu_item(item)
            saved_item = await self.menu_repository.create_item_menu(item, data.restaurant_id)
            if saved_item.is_error():
                return Result.failure(
                    error=saved_item.error,
                    messg=saved_item.messg
                )
            
            saved_item = saved_item.result()

            return Result.success(
                MenuItemResponse(
                restaurant_id=restaurant.get_id(),
                restaurant_name=restaurant.get_name(),
                item=MenuItemBase(
                    id=saved_item.get_id(),
                    name=saved_item.get_name(),
                    description=saved_item.get_description(),
                    category=saved_item.get_category()
                )
            ))
        except Exception as e:
            print(e)
            return Result.failure(
                error=e,
                messg="An error occurred while creating the menu item."
            )