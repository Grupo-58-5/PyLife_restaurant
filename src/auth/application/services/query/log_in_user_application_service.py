from src.shared.utils.i_application_service import IApplicationService
from src.auth.application.schemas.entry.log_in_schema_entry import LogInSchemaEntry
from src.auth.application.schemas.response.log_in_schema_response import LogInSchemaResponse
from src.auth.domain.repository.user_repository_interface import IUserRepository
from src.shared.application.ports.hash_handler import HashHelper as Hash
from src.shared.application.ports.auth_handler import AuthHandler as Auth
from src.shared.utils.result import Result

class LogInUserApplicationService(IApplicationService[LogInSchemaEntry,Result[LogInSchemaResponse]]):

    repo: IUserRepository
    hash: Hash
    auth_service: Auth

    def __init__(self, repo: IUserRepository, hash: Hash, auth_service: Auth):
        super().__init__()
        self.repo = repo
        self.hash = hash
        self.auth_service = auth_service

    async def execute(self, data: LogInSchemaEntry) -> Result[LogInSchemaResponse]:
        find_user = await self.repo.get_user_by_email(email=data.email)
        if find_user.is_error() is True:
            return Result[LogInSchemaResponse].failure(error=find_user.error,messg='Wrong email',code=403)
        user = find_user.value

        verify_password = await self.hash.verify_password(regular_password=data.password,hashed_password=user.get_password())
        if verify_password is False:
            return Result[LogInSchemaResponse].failure(BaseException,'Wrong password',403)

        token = await self.auth_service.sign(
            id=user.get_id(),
            role=user.get_role(),
            expire_time=None
        )

        result = LogInSchemaResponse(token=token)
        return Result[LogInSchemaResponse].success(result)