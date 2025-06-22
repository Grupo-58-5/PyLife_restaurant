


from fastapi import APIRouter
from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.restaurants.application.schemas.entry.create_table_schema import CreateTableSchema, UpdateTableSchema
from src.restaurants.application.schemas.entry.get_table_entry_schema import GetTableEntrySchema
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse, RestaurantTableResponse
from src.restaurants.application.services.commands.create_table_application_service import CreateTableApplicationService
from src.restaurants.application.services.commands.delete_table_application_service import DeleteTableApplicationService
from src.restaurants.application.services.commands.update_table_application_service import UpdateTableApplicationService
from src.restaurants.application.services.querys.get_all_table_application_service import GetAllTableApplicationService
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.restaurants.infraestructure.repository.table_repository_impl import TableRepositoryImpl
from src.shared.db.database import get_session

async def get_restaurant_repository(session: Session = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

async def get_table_repository(session: Session = Depends(get_session)) -> TableRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return TableRepositoryImpl(db=session)

router = APIRouter(prefix="/table", tags=["Tables"])

@router.get("/{restaurant_id}", summary="Get table by Restaurant ID", response_model=RestaurantTableResponse, status_code=status.HTTP_200_OK)
async def get_table(restaurant_id: UUID, restaurant_repo : RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo : TableRepositoryImpl = Depends(get_table_repository) ):
    """
    Retrieve the table for a specific restaurant.
    """
    service = GetAllTableApplicationService(restaurant_repo, table_repo)
    res = await service.execute(GetTableEntrySchema(restaurant_id=restaurant_id))
    if res.is_succes():
        return res.result()
    elif res.is_error():
        if res.get_error_code() == 404:
            raise HTTPException(status_code=404, detail=res.get_error_message())
        elif res.get_error_code() == 400:
            raise HTTPException(status_code=400, detail=res.get_error_message())
        elif res.get_error_code() == 500:
            raise HTTPException(status_code=500, detail=res.get_error_message())

@router.post("/{restaurant_id}", summary="Create table for a restaurant")
async def create_table(restaurant_id: UUID, table_data: CreateTableSchema, restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo: TableRepositoryImpl = Depends(get_table_repository) ):

    service = CreateTableApplicationService(table_repo, restaurant_repo)
    result = await service.execute(restaurant_id, table_data)
    if result.is_error():
        if result.get_error_code() != 500:
            raise HTTPException(status_code=result.get_error_code(), detail=result.get_error_message())
        raise HTTPException(status_code=500, detail=result.get_error_message())
    return result.result()

@router.put("/{restaurant_id}/{table_id}", summary="Update table by ID", status_code=status.HTTP_200_OK, response_model=BaseTableResponse)
async def update_table(restaurant_id: UUID, table_id: UUID, table_data: UpdateTableSchema, restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo: TableRepositoryImpl = Depends(get_table_repository)):

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

@router.delete("/{restaurant_id}/{table_number}", summary="Delete table by ID", status_code=status.HTTP_204_NO_CONTENT)
async def delete_table(restaurant_id: UUID, table_number: int , restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo: TableRepositoryImpl = Depends(get_table_repository)):
    service = DeleteTableApplicationService(table_repo, restaurant_repo)
    result = await service.execute((restaurant_id, table_number))
    if result.is_error():
        if result.get_error_code() != 500:
            raise HTTPException(status_code=result.get_error_code(), detail=result.get_error_message())
        raise HTTPException(status_code=500, detail=result.get_error_message())