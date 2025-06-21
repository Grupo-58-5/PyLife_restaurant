from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import Session
from typing import List, Annotated
from uuid import UUID

from src.auth.application.schemas.entry.delete_user_schema import DeleteUserSchema
from src.auth.application.schemas.entry.user_by_id_schema_entry import UserByIdSchemaEntry
from src.auth.application.services.delete_user_application_service import DeleteUserApplicationService
from src.auth.application.services.get_user_by_id_application_service import GetUserByIdApplicationService
from src.auth.domain.repository.user_repository_interface import IUserRepository
from src.shared.db.database import get_session
from src.auth.infraestructure.repository.user_repository_impl import UserRepositoryImpl
from src.auth.infraestructure.schemas.entry.sign_up_entry import SignUpEntry
from src.auth.application.schemas.entry.user_schema_entry import UserSchemaEntry
from src.auth.infraestructure.schemas.response.sign_up_response import SignUpResponse
from src.auth.application.schemas.entry.user_all_schema_entry import UserAllSchemaEntry
from src.auth.application.schemas.response.user_all_schema_response import UserAllSchemaeResponse
from src.auth.application.schemas.entry.log_in_schema_entry import LogInSchemaEntry
from src.auth.application.schemas.response.log_in_schema_response import LogInSchemaResponse
from src.auth.infraestructure.schemas.response.toke_schema import Token
from src.auth.application.services.create_user_application_service import CreateUserApplicationService
from src.auth.application.services.get_all_user_application_service import GetAllUserApplicationService
from src.auth.application.services.log_in_user_application_service import LogInUserApplicationService
from src.shared.application.ports.hash_handler import HashHelper
from src.shared.infraestructure.adapters.bcrypt_hash_adapter import BcryptHashAdapter
from src.shared.application.ports.auth_handler import AuthHandler
from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
# from src.auth.infraestructure.JWT.dependencies.get_user import GetUser
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.shared.utils.result import Result
from src.shared.db.database import TESTING
router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

auth = JWTAuthAdapter()

async def get_repository(session: AsyncSession = Depends(get_session)) -> UserRepositoryImpl:
    """Get an instance of the UserRepositoryImpl. """
    print("Session utilizado: ",session)
    print("Base de datos test: ",TESTING)
    return UserRepositoryImpl(db=session)

async def get_hash_password() -> HashHelper:
    """Get an instance of the BcryptHashAdapter. """
    return BcryptHashAdapter()

async def get_auth_adapter() -> AuthHandler:
    """Get an instance of the AuthAdapter. """
    return JWTAuthAdapter()

@router.post(
    "/sign_up",
    response_model=SignUpResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        409: {"description": "email already registered"}
    }
)
async def sign_up(
    body: SignUpEntry,
    repo: UserRepositoryImpl = Depends(get_repository),
    hash_helper: HashHelper = Depends(get_hash_password)
):
    """
    Create a new restaurant endpoint.
    """
    data = UserSchemaEntry.model_validate(body.model_dump())
    service = CreateUserApplicationService(repo=repo,hash=hash_helper)

    result = await service.execute(data=data)

    if result.is_error():

        if result.get_error_code() == 409:
            raise HTTPException(status_code=409, detail={'msg':str(result.get_error_message())})

        raise result.error

    response = SignUpResponse(message=result.value.message, role=result.value.role)

    return response

@router.post(
    "/log_in",
    status_code=status.HTTP_200_OK,
    response_model=Token,
    responses={
        403: {"description": "Wrong email"},
        403: {"description": "Wrong password"},
        403: {"description": "Wrong credentials"}
    }
)
async def log_in(
    body: Annotated[OAuth2PasswordRequestForm,Depends()],
    repo: UserRepositoryImpl = Depends(get_repository),
    hash_helper: HashHelper = Depends(get_hash_password),
    token_generator: AuthHandler = Depends(get_auth_adapter)
):

    """
    Log in into the account endpoint.
    """

    data = LogInSchemaEntry(
        email=body.username,
        password=body.password
    )

    service = LogInUserApplicationService(
        repo=repo,
        hash=hash_helper,
        auth_service=token_generator,
    )

    result = await service.execute(data)

    if result.is_error() is True:

        if result.get_error_code() == 403:
            raise HTTPException(status_code=result.get_error_code(),detail=result.get_error_message())

        raise result.error

    print(result.value)

    return Token(access_token=result.value.token, token_type="bearer")


@router.delete(
    "/delete/current_user",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write"],JWTAuthAdapter()))],
    description="Delete the user you log in with"
)
async def delete_current_user(
    info: Annotated[Result[dict],Depends(auth.decode)],
    repo: UserRepositoryImpl = Depends(get_repository),
):
    if info.is_error():
        raise HTTPException(status_code=500, detail=info.get_error_message())

    service = DeleteUserApplicationService(repo=repo)
    body = DeleteUserSchema(UUID(info.value.get('id')))
    result = await service.execute(body)

    if result.is_error() is True:
        raise HTTPException(status_code=500, detail=result.get_error_message())

    return {"msg":"Delete success"}

@router.delete(
    "/delete/user/{id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write"],JWTAuthAdapter()))],
    description="Delete a user by providing their ID"
)
async def delete_user(
    info: Annotated[dict,Depends(auth.decode)],
    id: str,
    repo: IUserRepository = Depends(get_repository),
):

    if info.is_error():
        raise HTTPException(status_code=500, detail=info.get_error_message())

    service = DeleteUserApplicationService(repo=repo)
    body = DeleteUserSchema(id=id)
    result = await service.execute(body)

    if result.is_error() is True:
        raise HTTPException(status_code=500, detail=result.get_error_message())

    return {"msg":"Delete success"}


