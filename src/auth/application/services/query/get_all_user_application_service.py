from typing import List

from src.auth.domain.user import User
from src.auth.domain.enum.role import Roles
from src.shared.utils.result import Result
from src.shared.utils.i_application_service import IApplicationService
from src.auth.application.schemas.entry.user_all_schema_entry import UserAllSchemaEntry
from src.auth.application.schemas.response.user_all_schema_response import UserAllSchemaeResponse
from src.auth.domain.repository.user_repository_interface import IUserRepository

class GetAllUserApplicationService(IApplicationService[UserAllSchemaEntry,Result[List[UserAllSchemaeResponse]]]):

    repo: IUserRepository

    def __init__(self, repo: IUserRepository):
        super().__init__()
        self.repo = repo

    async def execute(self, data: UserAllSchemaEntry) -> Result[List[UserAllSchemaeResponse]]:

        """
        Service to get all users registered in the database
        """

        users = (await self.repo.get_all(page=data.skip,page_size=data.limit)).value
        response = [UserAllSchemaeResponse(**u.__dict__()) for u in users]
        return Result[List[UserAllSchemaeResponse]].success(response)

