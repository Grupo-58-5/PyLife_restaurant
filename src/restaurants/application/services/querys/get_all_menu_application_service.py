



from src.restaurants.application.schemas.entry.get_menu_entry_schema import GetMenuEntrySchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItem
from src.restaurants.application.schemas.response.restaurant_menu_response import RestaurantMenuResponse
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService


class GetAllMenuApplicationService(IApplicationService[GetMenuEntrySchema, RestaurantMenuResponse]):
    """
    Service to retrieve the menu for a specific restaurant.
    """
    def __init__(self, restaurant_repository: IRestaurantRepository, menu_repository: IMenuRepository):
        super().__init__()
        self.restaurant_repository = restaurant_repository
        self.menu_repository = menu_repository

    async def execute( self, data: GetMenuEntrySchema ) -> RestaurantMenuResponse:
        try:
            restaurant = await self.restaurant_repository.get_restaurant_by_id(data.restaurant_id)

            menu = await self.menu_repository.get_menu(data.restaurant_id)

            return RestaurantMenuResponse(
                restaurant_id=restaurant.get_id(),
                restaurant_name=restaurant.get_name(),
                menu_items=[MenuItem(id=item.get_id(), name=item.get_name(), description=item.get_description(), category=item.get_category()) for item in menu]
            )
        except Exception as e:
            print(e)
            raise RuntimeError(f"Error retrieving menu: {str(e)}") from e