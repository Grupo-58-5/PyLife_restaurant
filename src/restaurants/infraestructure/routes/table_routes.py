


from fastapi import APIRouter
from uuid import uuid4, UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from src.restaurants.application.schemas.entry.create_table_schema import CreateTableSchema
from src.restaurants.application.schemas.entry.get_table_entry_schema import GetTableEntrySchema
from src.restaurants.application.schemas.entry.update_table_entry_schema import UpdateTableSchema
from src.restaurants.application.services.commands.create_table_application_service import CreateTableApplicationService
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

@router.get("/{restaurant_id}", summary="Get table by Restaurant ID")
async def get_table(restaurant_id: UUID, restaurant_repo : RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo : TableRepositoryImpl = Depends(get_table_repository) ):
    """
    Retrieve the table for a specific restaurant.
    """
    try:
        service = GetAllTableApplicationService(restaurant_repo, table_repo)
        res = await service.execute(GetTableEntrySchema(restaurant_id=restaurant_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    
@router.post("/{restaurant_id}", summary="Create table for a restaurant")
async def create_table(table_data: CreateTableSchema, restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository), table_repo: TableRepositoryImpl = Depends(get_table_repository) ):

    try:
        service = CreateTableApplicationService(table_repo, restaurant_repo)
        result = await service.execute(table_data)
        if result.is_error():
            raise HTTPException(status_code=400, detail=result.messg)
        return result.result()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.put("/{table_id}", summary="Update table by ID")
async def update_table(table_id: UUID, table_data: UpdateTableSchema, table_repo: TableRepositoryImpl = Depends(get_table_repository) ):

    try:
        service = UpdateTableApplicationService(table_repo)
        result = await service.execute((table_id, table_data))
        if result.is_error():
            raise HTTPException(status_code=400, detail=result.messg)
        return result.result()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.delete("/{table_id}", summary="Delete table by ID")
async def delete_table(table_id: UUID, table_repo: TableRepositoryImpl = Depends(get_table_repository) ):
    try:
        table_repo.delete_item_table(table_id)
        return {"message": "Table deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e