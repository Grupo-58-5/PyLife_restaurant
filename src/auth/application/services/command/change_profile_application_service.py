from src.auth.application.schemas.entry.change_profile_schema_entry import ChangeProfileSchemaEntry
from src.auth.application.schemas.response.change_profile_schema_response import ChangeProfileSchemaResponse
from src.auth.domain.repository.user_repository_interface import IUserRepository
from src.auth.domain.user import User
from src.auth.domain.value_object.user_email import UserEmail
from src.auth.domain.value_object.user_name import UserName
from src.auth.domain.value_object.user_password import UserPassword
from src.shared.application.ports.hash_handler import HashHelper
from src.shared.utils.i_application_service import IApplicationService
from src.shared.utils.result import Result


class ChangeProfileAplicationService(IApplicationService[ChangeProfileSchemaEntry,Result[ChangeProfileSchemaResponse]]):

    repo: IUserRepository
    hash: HashHelper

    def __init__(self, repo: IUserRepository, hash: HashHelper):
        super().__init__()
        self.repo = repo
        self.hash = hash

    async def execute(self, data: ChangeProfileSchemaEntry) -> Result[ChangeProfileSchemaResponse]:

        find_user_result = await self.repo.get_user_by_id(id=data.id)
        if find_user_result.is_error() is True:
            return Result[str].failure(error=find_user_result.error,messg=find_user_result.get_error_message(),code=404)

        user = find_user_result.value

        if data.email is not None:
            verify_email = await self.repo.verify_email(data.email)
            if(verify_email.value == True):
                return Result[str].failure(ValueError,'email already registered',409)
            user.change_email(UserEmail.create(data.email))
            print("Correo modificado")
        if data.password is not None:
            user.change_password(UserPassword.create(await self.hash.get_password_hashed(data.password)))
        if data.name is not None:
            user.change_name(UserName.create(data.name))

        print("Usario para actualizar: ",user)

        update = await self.repo.update_profile(user=user)

        if update.is_error() is True:
            return Result[str].failure(update.error,messg=update.get_error_message())

        response = ChangeProfileSchemaResponse(
            name=data.name if data.name is not None else None,
            email=data.email if data.email is not None else None,
            password=data.password if data.password is not None else None
        )

        return Result[ChangeProfileSchemaResponse].success(response)
