

from uuid import UUID
from src.restaurants.application.schemas.entry.create_table_schema import CreateTableSchema, UpdateTableSchema
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse
from src.restaurants.domain.entity.table_entity import TableEntity, TableLocation
from src.restaurants.domain.repository.i_restaurant_repository import IRestaurantRepository
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class UpdateTableApplicationService(IApplicationService[tuple[UUID, UpdateTableSchema], Result[BaseTableResponse]]):

    def __init__(self, table_repository: ITableRepository, restaurant_repository: IRestaurantRepository):
        super().__init__()
        self.table_repository = table_repository
        self.restaurant_repository = restaurant_repository

    async def execute(self, data: tuple[UUID, UpdateTableSchema]) -> Result[BaseTableResponse]:
        try:
            restaurant_id, table_data = data

            restaurant = await self.restaurant_repository.get_restaurant_by_id(restaurant_id)
            if restaurant is None:
                return Result.failure(
                    error=ValueError("Restaurant not found"),
                    messg=f"Restaurant with ID {restaurant_id} does not exist."
                )
            
            table_id = table_data.id
            if table_id is None:
                return Result.failure(
                    error=ValueError("Table ID is required for update"),
                    messg="Table ID must be provided for updating a table."
                )
            
            # Check if the table exists
            tables_in_restaurant = restaurant.get_tables()
            table_target = next((table for table in tables_in_restaurant if table.get_id() == table_id), None)
            if table_target is None:
                return Result.failure(
                    error=ValueError(f"Table with ID {table_id} not found in restaurant {restaurant_id}"),
                    messg=f"Table with ID {table_id} not found in restaurant {restaurant_id}."
                )
            tables_in_restaurant.remove(table_target)
            
            if table_data.table_number is not None:
                table_target.set_table_number(table_data.table_number)
            if table_data.seats is not None:
                table_target.set_seats(table_data.seats)
            if table_data.location is not None:
                table_target.set_location(TableLocation(table_data.location.value))
            
            restaurant.add_table(table_target)
            updated_table = await self.table_repository.update_item_table(table_id, table_target)
            if updated_table.is_error():
                return Result.failure(
                    error=updated_table.error,
                    messg=f"Error updating table: {updated_table.error.message}" if updated_table.error else "Error updating table"
                )
            updated_table = updated_table.result()
            return Result.success(
                BaseTableResponse(
                    table_number=updated_table.get_table_number(),
                    seats=updated_table.get_seats(),
                    location=updated_table.get_location()
                )
            )
        except ValueError as ve:
            if "Table with number" in str(ve):
                return Result.failure(error=ve, messg=str(ve), code=409)
            else:
                return Result.failure(error=ve, messg=str(ve), code=400)
        except Exception as e:
            return Result.failure(error=Exception(str(e)), messg=str(e), code=500)