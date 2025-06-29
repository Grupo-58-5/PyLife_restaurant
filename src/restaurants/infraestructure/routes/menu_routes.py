


from typing import Final
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.restaurants.application.schemas.entry.create_menu_item_schema import CreateMenuItemSchema, UpdateMenuSchema
from src.restaurants.application.schemas.entry.delete_menu_schema import DeleteMenuSchema
from src.restaurants.application.schemas.entry.get_menu_entry_schema import GetMenuEntrySchema
from src.restaurants.application.schemas.response.menu_item_response import MenuItemResponse
from src.restaurants.application.schemas.response.restaurant_menu_response import RestaurantMenuResponse
from src.restaurants.application.services.commands.delete_menu_application_service import DeleteMenuApplicationService
from src.restaurants.application.services.commands.update_menu_application_service import UpdateMenuApplicationService
from src.restaurants.application.services.querys.get_all_menu_application_service import GetAllMenuApplicationService
from src.restaurants.application.services.commands.create_menu_application_service import CreateMenuItemApplicationService
from src.restaurants.infraestructure.repository.menu_repository_impl import MenuRepositoryImpl
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.shared.db.database import get_session
from src.shared.utils.result import Result
from typing import Annotated



async def get_restaurant_repository(session: AsyncSession = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

async def get_menu_repository(session: AsyncSession = Depends(get_session)) -> MenuRepositoryImpl:
    """Get an instance of the MenuRepositoryImpl. """
    return MenuRepositoryImpl(db=session)


router = APIRouter(prefix="/menu", tags=["Menu"])
auth: Final = JWTAuthAdapter()

@router.get("/{restaurant_id}", summary="Get Menu by Restaurant ID",  response_model=RestaurantMenuResponse, status_code=status.HTTP_200_OK)
async def get_menu(restaurant_id: UUID, restaurant_repo : RestaurantRepositoryImpl = Depends(get_restaurant_repository) ):
    """
    Retrieve the menu for a specific restaurant.
    """
    service = GetAllMenuApplicationService(restaurant_repo)
    schema = GetMenuEntrySchema(restaurant_id=restaurant_id)
    res = await service.execute(schema)
    if res.is_succes():
        return res.result()
    else:
        raise HTTPException(status_code=400, detail=res.get_error_message) 

@router.post("/{restaurant_id}", summary="Create Menu Item",  response_model=MenuItemResponse, status_code=status.HTTP_201_CREATED)
async def create_menu_item(restaurant_id: UUID, menu: CreateMenuItemSchema, restaurant_repo : RestaurantRepositoryImpl = Depends(get_restaurant_repository), menu_repo : MenuRepositoryImpl = Depends(get_menu_repository)):
    """
    Create a new menu item for a specific restaurant.
    """
    service = CreateMenuItemApplicationService(menu_repo, restaurant_repo)
    menu.restaurant_id = restaurant_id
    res = await service.execute(menu)
    if res.is_succes():
        return res.result()
    if res.is_error():
        if res.get_error_code() != 500:
            raise HTTPException(status_code= res.get_error_code(), detail=str(res.get_error_message()))
        else:
            raise HTTPException(status_code=500, detail="Unexpected error")
    

@router.delete("/{restaurant_id}", status_code=status.HTTP_200_OK, response_model=MenuItemResponse, summary="Delete Menu Item")    
async def delete_menu_item(restaurant_id: UUID, menu_id:UUID, restaurant_repo : RestaurantRepositoryImpl = Depends(get_restaurant_repository), menu_repo: MenuRepositoryImpl = Depends(get_menu_repository)):

    service = DeleteMenuApplicationService(restaurant_repo,menu_repo)
    schema = DeleteMenuSchema(restaurant_id=restaurant_id, menu_id=menu_id)
    res = await service.execute(schema)
    if res.is_succes():
        return res.result()
    else:
        raise HTTPException(status_code=400, detail=res.get_error_message())
    

@router.put(
    "/{restaurant_id}/menu/{menu_id}",
    summary="Update a menu item by ID",
    status_code=status.HTTP_200_OK,
    response_model=MenuItemResponse,
)
async def update_menu_item(
    restaurant_id: UUID,
    menu_id: UUID,
    menu_data: UpdateMenuSchema,
    restaurant_repo: RestaurantRepositoryImpl = Depends(get_restaurant_repository),
    menu_repo: MenuRepositoryImpl = Depends(get_menu_repository),
):
    service = UpdateMenuApplicationService(menu_repo, restaurant_repo)
    result = await service.execute((restaurant_id, menu_id, menu_data))

    if result.is_error():
        raise HTTPException(
            status_code=result.get_error_code() or 400,
            detail=result.get_error_message()
        )

    return result.result()    