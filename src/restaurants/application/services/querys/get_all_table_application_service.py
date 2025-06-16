

from src.restaurants.application.schemas.entry.get_table_entry_schema import GetTableEntrySchema
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse, RestaurantTableResponse
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService


class GetAllTableApplicationService(IApplicationService[GetTableEntrySchema, RestaurantTableResponse]):
    """
    Service to retrieve the table for a specific restaurant.
    """
    def __init__(self, restaurant_repository: IRestaurantRepository, table_repository: ITableRepository):
        super().__init__()
        self.restaurant_repository = restaurant_repository
        self.table_repository = table_repository

    async def execute( self, data: GetTableEntrySchema ) -> RestaurantTableResponse:
        try:
            restaurant = await self.restaurant_repository.get_restaurant_by_id(data.restaurant_id)

            table = await self.table_repository.get_table(data.restaurant_id)
            return RestaurantTableResponse(
                restaurant_id=restaurant.get_id(),
                restaurant_name=restaurant.get_name(),
                table_item=[BaseTableResponse(id=item.get_id(), table_number=item.get_table_number(), seats=item.get_seats(), location=item.get_location()) for item in table]
            )
        except Exception as e:
            print(e)
            raise RuntimeError(f"Error retrieving menu: {str(e)}") from e