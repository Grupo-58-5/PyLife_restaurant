from typing import Annotated, Final
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.infraestructure.JWT.JWT_auth_adapter import JWTAuthAdapter
from src.auth.infraestructure.JWT.dependencies.verify_scope import VerifyScope
from src.restaurants.application.services.commands.create_restaurant_application_service import CreateRestaurantApplicationService
from src.restaurants.application.services.commands.delete_restaurant_application_service import DeleteRestaurantApplicationService
from src.restaurants.application.services.commands.update_restaurant_application_service import UpdateRestaurantApplicationService
from src.restaurants.application.services.querys.get_all_restaurant_application_sevice import GetAllRestaurantApplicationService
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema, UpdateRestaurantSchema
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse, RestaurantDetailResponse


from src.shared.db.database import get_session
from src.shared.utils.result import Result

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])
auth: Final = JWTAuthAdapter()

async def get_repository(session: AsyncSession = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

@router.get(
    "/", response_model=list[BaseRestaurantResponse],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write","client:write","client:read"],auth))]
)
async def get_restaurants(info: Annotated[Result[dict],Depends(auth.decode)], repo : RestaurantRepositoryImpl = Depends(get_repository)):

    service = GetAllRestaurantApplicationService(repo)
    res= await service.execute()
    print("Response from get_restaurants: ", res)
    if res.is_error():
        raise HTTPException(status_code=500, detail=str(res.get_error_message()))
    
    return res.result()

@router.post(
    "/",
    response_model=RestaurantDetailResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(VerifyScope(["admin:read","admin:write"],auth))]
)
async def create_restaurant(info: Annotated[Result[dict],Depends(auth.decode)], restaurant: CreateRestaurantSchema, repo: RestaurantRepositoryImpl = Depends(get_repository)):
    """
    Create a new restaurant endpoint.
    """

    service = CreateRestaurantApplicationService(repo)
    res = await service.execute(restaurant)
    if res.is_error():
        if res.get_error_code() == 400:
            raise HTTPException(status_code=400, detail=str(res.get_error_message()))
        else:
            raise HTTPException(status_code=500, detail="Unexpected error")
    return res.result()

@router.patch(
    "/{restaurant_id}",
    summary="Update restaurant by ID",
    status_code=status.HTTP_200_OK,
    response_model=RestaurantDetailResponse,
    dependencies=[Depends(VerifyScope(["admin:write"], auth))]
)
async def update_restaurant(
    restaurant_id: UUID,
    update_data: UpdateRestaurantSchema,
    info: Annotated[Result[dict], Depends(auth.decode)],
    restaurant_repo: RestaurantRepositoryImpl = Depends(get_repository)
):
    
    service = UpdateRestaurantApplicationService(restaurant_repo)
    update_data = UpdateRestaurantSchema(
        name=update_data.name if update_data.name is not None else None,
        address=update_data.address if update_data.address is not None else None,
        opening_time=update_data.opening_time if update_data.opening_time is not None else None,
        closing_time=update_data.closing_time if update_data.closing_time is not None else None
    )

    result = await service.execute([restaurant_id, update_data])

    if result.is_error():
        if result.get_error_code() != 500:
            raise HTTPException(status_code=result.get_error_code() or 500, detail=result.get_error_message())
        raise HTTPException(status_code=500, detail=result.get_error_message())
    return result.result()


@router.delete(
    "/{restaurant_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(VerifyScope(["admin:write"], auth))]
)
async def delete_restaurant(restaurant_id: UUID, info: Annotated[Result[dict], Depends(auth.decode)],repo: RestaurantRepositoryImpl = Depends(get_repository)):
    """
    Delete a restaurant by ID (accessible to administrators only).
    """
    service = DeleteRestaurantApplicationService(repo)
    res = await service.execute(restaurant_id)
    if res.is_error():
        if res.get_error_code() != 500:
            raise HTTPException(status_code=res.get_error_code() or 500, detail=res.get_error_message())
        raise HTTPException(status_code=500, detail=res.get_error_message())