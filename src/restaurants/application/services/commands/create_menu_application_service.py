


from uuid import uuid4
from src.restaurants.application.schemas.entry.create_menu_item_schema import CreateMenuItemSchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItem, MenuItemResponse
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.entity.menu_entity import MenuEntity
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService


class CreateMenuItemApplicationService(IApplicationService[CreateMenuItemSchema, MenuItemResponse]):
    """
    Service class responsible for handling the creation of menu items within a restaurant context.
    """
    def __init__(self, menu_repository: IMenuRepository, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.menu_repository = menu_repository
        self.restaurant_repository = restaurant_repository

    async def execute(self, data: CreateMenuItemSchema) -> MenuItemResponse:
        try:
            item_id = uuid4()
            item = MenuEntity(
                id=item_id,
                name=data.name,
                description=data.description,
                category=data.category
            )
            saved_item = await self.menu_repository.create_item_menu(item, data.restaurant_id)

            restaurant = await self.restaurant_repository.get_restaurant_by_id(data.restaurant_id)

            return MenuItemResponse(
                restaurant_id=restaurant.id,
                restaurant_name=restaurant.name,
                item=MenuItem(
                    id=saved_item.id,
                    name=saved_item.name,
                    description=saved_item.description,
                    category=saved_item.category
                )
                
            )
        
        except Exception as e:
            print(e)
            raise Exception(f"Error creating menu item: {str(e)}, {e.__cause__}") from e