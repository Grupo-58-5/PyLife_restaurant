from uuid import UUID
from src.restaurants.domain.repository.i_table_repository import ITableRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result

class DeleteTableApplicationService(IApplicationService[UUID, Result[bool]]):
    def __init__(self, table_repository: ITableRepository):
        super().__init__()
        self.table_repository = table_repository

    async def execute(self, table_id: UUID) -> Result[bool]:
        try:
            result = self.table_repository.delete_item_table(table_id)
            if result.is_error():
                return Result.failure(
                    error=result.error,
                    messg=result.messg
                )
            return Result.success(True)
        except Exception as e:
            return Result.failure(Exception(str(e)), str(e), 500)
            