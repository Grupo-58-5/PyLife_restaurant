from uuid import UUID
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class DeleteTableApplicationService(IApplicationService[tuple[UUID, int], Result[bool]]):
    def __init__(self, table_repository: ITableRepository, restaurant_repository=IRestaurantRepository):
        super().__init__()
        self.table_repository = table_repository
        self.restaurant_repository = restaurant_repository

    async def execute(self, data: tuple[UUID, int]) -> Result[bool]:
        try:
            restaurant_id, table_number = data
            restaurant = await self.restaurant_repository.get_restaurant_by_id(restaurant_id)
            if restaurant is None:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {restaurant_id} does not exist."
                )
            
            
            tables = restaurant.get_tables()
            if not tables:
                return Result.failure(
                    error=ValueError("No tables found"),
                    messg=f"No tables found for restaurant with ID {restaurant_id}."
                )
            table_id = None
            for table in tables:
                if table.get_table_number() == table_number:
                    table_id = table.get_id()
                    break
            if table_id is None:
                return Result.failure(
                    error=ValueError("Table not found"),
                    messg=f"Table with number {table_number} does not exist in restaurant with ID {restaurant_id}."
                )
            
            #? # Delete the table
            result = await self.table_repository.delete_item_table(table_id)
            if result.is_error():
                return Result.failure(
                    status_code=404,
                    error=result.error,
                    messg=result.messg
                )
            return Result.success(True)
        except Exception as e:
            return Result.failure(Exception(str(e)), str(e), 500)
            