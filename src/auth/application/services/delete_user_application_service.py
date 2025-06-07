from src.auth.application.schemas.entry.delete_user_schema import DeleteUserSchema
from src.auth.domain.repository.user_repository_interface import IUserRepository
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class DeleteUserApplicationService(IApplicationService[DeleteUserSchema,Result[bool]]):

    repo: IUserRepository

    def __init__(self,repo: IUserRepository):
        super().__init__()
        self.repo = repo

    async def execute(self, data) -> Result[bool]:

        """
        Service to delete a specific user by the id
        """

        find_user_result = await self.repo.get_user_by_id(id=str(data.id))
        if find_user_result.is_error() is True:
            return Result[bool].failure(error=find_user_result.error,messg=find_user_result.get_error_message(),code=404)

        user = find_user_result.value
        delete = await self.repo.delete_user(user=user)
        if delete.is_error() is True:
            return Result[bool].failure(error=delete.error,messg=delete.get_error_message())
        return Result[bool].success(True)
