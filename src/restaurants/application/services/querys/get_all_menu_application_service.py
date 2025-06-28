



from src.restaurants.application.schemas.entry.get_menu_entry_schema import GetMenuEntrySchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItem, MenuItemBase
from src.restaurants.application.schemas.response.restaurant_menu_response import RestaurantMenuResponse
from src.restaurants.domain.repository.i_menu_repository import IMenuRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class GetAllMenuApplicationService(IApplicationService[GetMenuEntrySchema, Result[RestaurantMenuResponse]]):
    """
    Service to retrieve the menu for a specific restaurant.
    """
    def __init__(self, restaurant_repository: IRestaurantRepository, menu_repository: IMenuRepository):
        super().__init__()
        self.restaurant_repository = restaurant_repository
        self.menu_repository = menu_repository

    async def execute( self, data: GetMenuEntrySchema ) -> Result[RestaurantMenuResponse]:
        try:
            restaurant = await self.restaurant_repository.get_restaurant_by_id(data.restaurant_id)
            if not restaurant:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {data.restaurant_id} does not exist."
                )

            # menu = await self.menu_repository.get_menu(data.restaurant_id)
            return Result.success(
                RestaurantMenuResponse(
                restaurant_id=restaurant.get_id(),
                restaurant_name=restaurant.get_name(),
                menu_items=[MenuItemBase(id=item.get_id(), name=item.get_name(), description=item.get_description(), category=item.get_category()) for item in restaurant.get_menu()]
            ))
        except Exception as e:
            print(e)
            return Result.failure(
                error=ValueError("Something wrong happend getting menu for the restaurant"), 
                messg=f"Restaurant with ID {data.restaurant_id} does not exist."
            )