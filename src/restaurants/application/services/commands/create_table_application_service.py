from uuid import UUID, uuid4
from src.restaurants.application.schemas.entry.create_table_schema import CreateTableSchema
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse
from src.restaurants.domain.entity.table_entity import TableEntity, TableLocation
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class CreateTableApplicationService(IApplicationService[CreateTableSchema, Result[BaseTableResponse]]):
    """
    Service to create a table for a specific restaurant.
    """
    def __init__(self, table_repository: ITableRepository, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.table_repository = table_repository
        self.restaurant_repository = restaurant_repository

    async def execute(self, restaurant_id: UUID, data: CreateTableSchema) -> Result[BaseTableResponse]:
        try:
            restaurant = await self.restaurant_repository.get_restaurant_by_id(restaurant_id)
            if restaurant is None:
                # If the restaurant does not exist, return a failure result
                return Result.failure(
                    code=404,
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {restaurant_id} does not exist."
                )
            
            table = TableEntity.create(
                id=uuid4(),
                table_number=data.table_number,
                seats=data.seats,
                location=data.location.value
            )
            
            restaurant.add_table(table)
            saved_table = await self.table_repository.create_item_table(table, restaurant_id)
            if saved_table.is_error():
                return Result.failure(
                    code=404,
                    error=saved_table.error,
                    messg=f"Error saving table: {saved_table.error.message}" if saved_table.error else "Error saving table"
                )
            
            saved_table = saved_table.result()
            return Result.success(
                BaseTableResponse(
                    id=saved_table.get_id(),
                    table_number=saved_table.get_table_number(),
                    seats=saved_table.get_seats(),
                    location=saved_table.get_location()
                )
            )
        except ValueError as ve:
            if "Table with number" in str(ve):
                return Result.failure(error=ve, messg=str(ve), code=409)
            else:
                return Result.failure(error=ve, messg=str(ve), code=400)
        except Exception as e:
            return Result.failure(error=Exception(str(e)), messg=str(e), code=500)