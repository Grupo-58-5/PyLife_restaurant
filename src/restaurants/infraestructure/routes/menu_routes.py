


from typing import Annotated, Final
from fastapi import APIRouter
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.restaurants.application.schemas.entry.create_menu_item_schema import CreateMenuItemSchema
from src.restaurants.application.schemas.entry.get_menu_entry_schema import GetMenuEntrySchema
from src.restaurants.application.services.querys.get_all_menu_application_service import GetAllMenuApplicationService
from src.restaurants.application.services.commands.create_menu_application_service import CreateMenuItemApplicationService
from src.restaurants.infraestructure.repository.menu_repository_impl import MenuRepositoryImpl
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.shared.db.database import get_session
from src.shared.utils.result import Result


async def get_restaurant_repository(session: AsyncSession = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

async def get_menu_repository(session: AsyncSession = Depends(get_session)) -> MenuRepositoryImpl:
    """Get an instance of the MenuRepositoryImpl. """
    return MenuRepositoryImpl(db=session)


router = APIRouter(prefix="/menu", tags=["Menu"])
auth: Final = JWTAuthAdapter()

@router.get("/{restaurant_id}", summary="Get Menu by Restaurant ID")
async def get_menu(restaurant_id: UUID, info: Annotated[Result[dict],Depends(auth.decode)],restaurant_repo : RestaurantRepositoryImpl = Depends(get_restaurant_repository), menu_repo : MenuRepositoryImpl = Depends(get_menu_repository) ):
    """
    Retrieve the menu for a specific restaurant.
    """
    try:
        service = GetAllMenuApplicationService(restaurant_repo, menu_repo)
        res = await service.execute(GetMenuEntrySchema(restaurant_id=restaurant_id))
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.post(
    "/{restaurant_id}",
    summary="Create Menu Item",
    dependencies=[Depends(VerifyScope(["admin:read","admin:write"],auth))]
)
async def create_menu_item(restaurant_id: UUID, menu: CreateMenuItemSchema, info: Annotated[Result[dict],Depends(auth.decode)],restaurant_repo : RestaurantRepositoryImpl = Depends(get_restaurant_repository), menu_repo : MenuRepositoryImpl = Depends(get_menu_repository)):
    """
    Create a new menu item for a specific restaurant.
    """
    service = CreateMenuItemApplicationService(menu_repo, restaurant_repo)
    menu.restaurant_id = restaurant_id
    res = await service.execute(menu)
    if res.is_succes():
        return res.result()
    else:
        raise HTTPException(status_code=400, detail=res.get_error_message())
