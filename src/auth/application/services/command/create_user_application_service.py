from uuid import uuid4, UUID

from src.auth.domain.user import User
from src.auth.domain.value_object.user_email import UserEmail
from src.auth.domain.value_object.user_name import UserName
from src.auth.domain.value_object.user_password import UserPassword
from src.auth.infraestructure.model.user_model import UserModel
from src.auth.domain.enum.role import Roles
from src.shared.utils.result import Result
from src.shared.utils.i_application_service import IApplicationService
from src.auth.application.schemas.entry.user_schema_entry import UserSchemaEntry
from src.auth.application.schemas.response.user_schema_response import UserSchemaeResponse
from src.auth.domain.repository.user_repository_interface import IUserRepository
from src.shared.application.ports.hash_handler import HashHelper

class CreateUserApplicationService(IApplicationService[UserSchemaEntry,Result[UserSchemaeResponse]]):

    repo: IUserRepository
    hash: HashHelper

    def __init__(self, repo: IUserRepository,hash: HashHelper):
        super().__init__()
        self.repo = repo
        self.hash = hash

    async def execute(self, data: UserSchemaEntry) -> Result[UserSchemaeResponse]:

        """
        Service to register a new user
        """

        verify = await self.repo.verify_email(data.email)

        if(verify.value == True):
            print("Usuario ya registrado")
            return Result[User].failure(ValueError,'email already registered',409)

        user_id: UUID = uuid4()
        password_hash = await self.hash.get_password_hashed(data.password)
        user = User(
            user_id,
            UserName.create(data.name),
            UserEmail.create(data.email),
            UserPassword.create(password_hash),
            Roles.CLIENT
        )

        save: Result[User] = await self.repo.create_user(user=user)

        if save.is_error():
            return Result[UserSchemaeResponse].failure(save.error,save.messg)

        response = UserSchemaeResponse(id=str(user_id),role=user.get_role(),message=f'Registered user')

        return Result[UserSchemaeResponse].success(response)
