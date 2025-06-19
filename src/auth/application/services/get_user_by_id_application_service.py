from typing import List

from src.auth.application.schemas.entry.user_by_id_schema_entry import UserByIdSchemaEntry
from src.auth.domain.user import User
from src.auth.domain.enum.role import Roles
from src.shared.utils.result import Result
from src.shared.utils.i_application_service import IApplicationService
from src.auth.application.schemas.response.user_all_schema_response import UserAllSchemaeResponse
from src.auth.domain.repository.user_repository_interface import IUserRepository

class GetUserByIdApplicationService(IApplicationService[UserByIdSchemaEntry,Result[UserAllSchemaeResponse]]):

    repo: IUserRepository

    def __init__(self, repo: IUserRepository):
        super().__init__()
        self.repo = repo

    async def execute(self, data: UserByIdSchemaEntry) -> Result[UserAllSchemaeResponse]:

        """
        Service to get user registered in the database by ID
        """

        find_user_result = await self.repo.get_user_by_id(id=str(data.id))
        if find_user_result.is_error() is True:
            return Result[bool].failure(error=find_user_result.error,messg=find_user_result.get_error_message(),code=404)

        user = find_user_result.value

        return Result[UserAllSchemaeResponse].success(UserAllSchemaeResponse(**user.__dict__()))


