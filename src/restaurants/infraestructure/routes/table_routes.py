


from typing import Annotated, Final, Optional
from fastapi import APIRouter
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.restaurants.application.schemas.entry.create_table_schema import CreateTableSchema, TableLocation, UpdateTableSchema
from src.restaurants.application.schemas.entry.get_table_entry_schema import GetTableEntrySchema
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse, RestaurantTableResponse, TableDetailsResponse
from src.restaurants.application.services.commands.create_table_application_service import CreateTableApplicationService
from src.restaurants.application.services.commands.delete_table_application_service import DeleteTableApplicationService
from src.restaurants.application.services.commands.update_table_application_service import UpdateTableApplicationService
from src.restaurants.application.services.querys.get_all_table_application_service import GetAllTableApplicationService
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.restaurants.infraestructure.repository.table_repository_impl import TableRepositoryImpl
from src.shared.db.database import get_session
from src.shared.utils.result import Result

async def get_restaurant_repository(session: Session = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

async def get_table_repository(session: Session = Depends(get_session)) -> TableRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return TableRepositoryImpl(db=session)

router = APIRouter(prefix="/table", tags=["Tables"])
auth: Final = JWTAuthAdapter()

# Query parameters are defined directly in the endpoint function signatures.

@router.get(
    "/{restaurant_id}",
    summary="Get table by Restaurant ID",
    response_model=RestaurantTableResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write","client:write","client:read"],auth))]
)
async def get_table(
    restaurant_id: UUID,
    info: Annotated[Result[dict], Depends(auth.decode)],
    restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository),
    table_repo: TableRepositoryImpl = Depends(get_table_repository),
    location: TableLocation | None = None,
    capacity: int = 2
):
    """
    Retrieve the table for a specific restaurant.
    """
    print(f"restaurant_id: {restaurant_id}, location: {location}, capacity: {capacity}")
    service = GetAllTableApplicationService(restaurant_repo, table_repo)
    res = await service.execute(
        GetTableEntrySchema(
            restaurant_id=restaurant_id,
            location=location.value if location else None,
            capacity=capacity
        )
    )
    if res.is_succes():
        return res.result()
    elif res.is_error():
        if res.get_error_code() == 404:
            raise HTTPException(status_code=404, detail=res.get_error_message())
        elif res.get_error_code() == 400:
            raise HTTPException(status_code=400, detail=res.get_error_message())
        elif res.get_error_code() == 500:
            raise HTTPException(status_code=500, detail=res.get_error_message())


@router.post(
    "/{restaurant_id}",
    summary="Create table for a restaurant",
    status_code=status.HTTP_201_CREATED,
    response_model=TableDetailsResponse,
    dependencies=[Depends(VerifyScope(["admin:read",'admin:write'], auth))]
)
async def create_table(restaurant_id: UUID, table_data: CreateTableSchema, info: Annotated[Result[dict],Depends(auth.decode)],restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo: TableRepositoryImpl = Depends(get_table_repository) ):

    service = CreateTableApplicationService(table_repo, restaurant_repo)
    result = await service.execute(restaurant_id, table_data)
    if result.is_error():
        if result.get_error_code() != 500:
            raise HTTPException(status_code=result.get_error_code(), detail=result.get_error_message())
        raise HTTPException(status_code=500, detail=result.get_error_message())
    return result.result()

@router.put(
    "/{restaurant_id}/{table_id}",
    summary="Update table by ID",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=TableDetailsResponse,
    dependencies=[Depends(VerifyScope(["admin:read",'admin:write'],auth))]
)
async def update_table(restaurant_id: UUID, table_id: UUID, table_data: UpdateTableSchema, info: Annotated[Result[dict],Depends(auth.decode)],restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo: TableRepositoryImpl = Depends(get_table_repository)):

    service = UpdateTableApplicationService(table_repo, restaurant_repo)
    table_data = UpdateTableSchema(
        id=table_id,
        table_number=table_data.table_number if table_data.table_number is not None else None,
        seats=table_data.seats if table_data.seats is not None else None,
        location=table_data.location.value if table_data.location else None
    )
    result = await service.execute((restaurant_id, table_data))
    if result.is_error():
        if result.get_error_code() != 500:
            raise HTTPException(status_code=result.get_error_code(), detail=result.get_error_message())
        raise HTTPException(status_code=500, detail=result.get_error_message())
    return result.result()

## TODO: Check application service for delete table, must not be referenced in reservations
@router.delete(
    "/{restaurant_id}/{table_number}",
    summary="Delete table by ID",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(VerifyScope(["admin:read",'admin:write'],auth))]
)
async def delete_table(restaurant_id: UUID, table_number: int , info: Annotated[Result[dict],Depends(auth.decode)],restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo: TableRepositoryImpl = Depends(get_table_repository)):
    service = DeleteTableApplicationService(table_repo, restaurant_repo)
    result = await service.execute((restaurant_id, table_number))
    if result.is_error():
        if result.get_error_code() != 500:
            raise HTTPException(status_code=result.get_error_code(), detail=result.get_error_message())
        raise HTTPException(status_code=500, detail=result.get_error_message())