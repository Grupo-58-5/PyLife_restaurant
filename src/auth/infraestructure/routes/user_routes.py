from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.auth.application.schemas.entry.change_profile_schema_entry import ChangeProfileSchemaEntry
from src.auth.application.schemas.entry.user_all_schema_entry import UserAllSchemaEntry
from src.auth.application.schemas.entry.user_by_id_schema_entry import UserByIdSchemaEntry
from src.auth.application.schemas.response.user_all_schema_response import UserAllSchemaeResponse
from src.auth.application.services.change_profile_application_service import ChangeProfileAplicationService
from src.auth.application.services.get_all_user_application_service import GetAllUserApplicationService
from src.auth.application.services.get_user_by_id_application_service import GetUserByIdApplicationService
from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.auth.infraestructure.repository.user_repository_impl import UserRepositoryImpl
from src.auth.infraestructure.schemas.entry.change_profile_entry import ChangeProfileEntry
from src.shared.application.ports.auth_handler import AuthHandler
from src.shared.application.ports.hash_handler import HashHelper
from src.shared.db.database import get_session
from src.shared.infraestructure.adapters.bcrypt_hash_adapter import BcryptHashAdapter
from src.shared.utils.result import Result


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

auth = JWTAuthAdapter()

async def get_repository(session: Session = Depends(get_session)) -> UserRepositoryImpl:
    """Get an instance of the UserRepositoryImpl. """
    print("Session utilizado: ",session)
    return UserRepositoryImpl(db=session)

async def get_hash_password() -> HashHelper:
    """Get an instance of the BcryptHashAdapter. """
    return BcryptHashAdapter()

async def get_auth_adapter() -> AuthHandler:
    """Get an instance of the AuthAdapter. """
    return JWTAuthAdapter()

@router.get(
    "/get/users",
    response_model=List[UserAllSchemaeResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["admin:read",'client:read'],JWTAuthAdapter()))]
)
async def get_all(
    info: Annotated[Result[dict],Depends(auth.decode)],
    query: UserAllSchemaEntry = Depends(),
    repo: UserRepositoryImpl = Depends(get_repository),
):
    """
    Get all users endpoint.
    """

    if info.is_error():
        raise HTTPException(status_code=500, detail=info.get_error_message())


    service = GetAllUserApplicationService(repo=repo)

    result = await service.execute(query)

    return result.value

@router.get(
    "/get/{id}",
    response_model=UserAllSchemaeResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["admin:read"],JWTAuthAdapter()))]
)
async def get_user(
    id: str,
    info: Annotated[Result[dict],Depends(auth.decode)],
    repo: UserRepositoryImpl = Depends(get_repository)
):
    """
    Get user by ID endpoint.
    """

    if info.is_error():
        raise HTTPException(status_code=500, detail=info.get_error_message())


    service = GetUserByIdApplicationService(repo=repo)

    result = await service.execute(UserByIdSchemaEntry(id=id))

    return result.value

@router.patch(
    "/change/profile",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["client:write","client:read","admin:write","admin:read"],JWTAuthAdapter()))]
)
async def update_profile(
    body: ChangeProfileEntry,
    info: Annotated[Result[dict],Depends(auth.decode)],
    repo: UserRepositoryImpl = Depends(get_repository),
    hash: HashHelper = Depends(get_hash_password)
):
    """
    Update profile of current user.
    """

    if info.is_error():
        raise HTTPException(status_code=500, detail=info.get_error_message())

    data = ChangeProfileSchemaEntry(id=info.value.get('id'),**body.__dict__)

    service = ChangeProfileAplicationService(repo=repo,hash=hash)

    result = await service.execute(data)

    return {'msg':result.value}
