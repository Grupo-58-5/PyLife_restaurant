

from src.restaurants.application.schemas.entry.get_table_entry_schema import GetTableEntrySchema
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse, RestaurantTableResponse
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class GetAllTableApplicationService(IApplicationService[GetTableEntrySchema, Result[RestaurantTableResponse]]):
    """
    Service to retrieve the table for a specific restaurant.
    """
    def __init__(self, restaurant_repository: IRestaurantRepository, table_repository: ITableRepository):
        super().__init__()
        self.restaurant_repository = restaurant_repository
        self.table_repository = table_repository

    async def execute( self, data: GetTableEntrySchema ) -> Result[RestaurantTableResponse]:
        try:
            restaurant = await self.restaurant_repository.get_restaurant_by_id(data.restaurant_id)
            if not restaurant:
                return Result.failure(
                    error=Exception("Restaurant not found"),
                    messg=f"Restaurant with ID {data.restaurant_id} does not exist.",
                    error_code=404
                )
            
            response_tables = []
            if data.location is not None: 
                response_tables = [table for table in restaurant.get_tables() if table.get_location() == data.location.value and table.get_seats() >= data.capacity] 
            else:
                response_tables = [table for table in restaurant.get_tables() if table.get_seats() >= data.capacity]

            
            return Result.success(
                RestaurantTableResponse(
                restaurant_id=restaurant.get_id(),
                restaurant_name=restaurant.get_name(),
                tables=[
                    BaseTableResponse(
                        table_number=item.get_table_number(), 
                        seats=item.get_seats(), 
                        location=item.get_location()) for item in response_tables])
            )
        except ValueError as ve:
            print(ve)
            return Result.failure(
                error=ve,
                messg=f"Invalid data provided: {ve}",
                error_code=400
            )
        except Exception as e:
            print(e)
            return Result.failure(
                error=Exception('Error retrieving tables'),
                messg=f'Something strange happened retrieving tables: {e}',
                error_code=500
            )