

from uuid import UUID
from src.restaurants.application.schemas.entry.create_table_schema import CreateTableSchema
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse
from src.restaurants.domain.entity.table_entity import TableEntity, TableLocation
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class UpdateTableApplicationService(IApplicationService[tuple[UUID, CreateTableSchema], Result[BaseTableResponse]]):

    def __init__(self, table_repository: ITableRepository):
        super().__init__()
        self.table_repository = table_repository

    async def execute(self, data: tuple[UUID, CreateTableSchema]) -> Result[BaseTableResponse]:
        try:
            table_id, table_data = data

            tables = await self.table_repository.get_table_by_id(table_id)
            if not tables:
                return Result.failure(
                    error=ValueError("Table not found"),
                    messg=f"Table with ID {table_id} does not exist."
                )

            updated_entity = TableEntity.create(
                id=table_id,
                table_number=table_data.table_number,
                seats=table_data.seats,
                location=table_data.location
            )

            result = self.table_repository.update_item_table(table_id, updated_entity)
            if result.is_error():
                return Result.failure(
                    error=result.error,
                    messg=result.messg
                )
            
            updated_table = result.result()
            return Result.success(
                BaseTableResponse(
                    id=updated_table.get_id(),
                    table_number=updated_table.get_table_number(),
                    seats=updated_table.get_seats(),
                    location=updated_table.get_location()
                )
            )
        except Exception as e:
            return Result.failure(Exception(str(e)), str(e), 500)