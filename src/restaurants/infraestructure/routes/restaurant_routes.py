from fastapi import APIRouter, Depends, HTTPException, status

from sqlmodel.ext.asyncio.session import AsyncSession
from src.restaurants.application.services.commands.create_restaurant_application_service import CreateRestaurantApplicationService
from src.restaurants.application.services.querys.get_all_restaurant_application_sevice import GetAllRestaurantApplicationService
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse, RestaurantDetailResponse


from src.shared.db.database import get_session

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

async def get_repository(session: AsyncSession = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

@router.get("/", response_model=list[BaseRestaurantResponse], status_code=status.HTTP_200_OK)
async def get_restaurants(repo : RestaurantRepositoryImpl = Depends(get_repository)):
    try:
        service = GetAllRestaurantApplicationService(repo)
        res= await service.execute()
        return res
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve)) from ve
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@router.post("/", response_model=RestaurantDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: CreateRestaurantSchema, repo: RestaurantRepositoryImpl = Depends(get_repository)):
    """
    Create a new restaurant endpoint.
    """
    
    service = CreateRestaurantApplicationService(repo)
    res = await service.execute(restaurant)
    if res.is_error():
        if res.get_error_code() == 400:
            print('csm')
            raise HTTPException(status_code=400, detail=str(res.get_error_message()))
        else:
            raise HTTPException(status_code=500, detail="Unexpected error")
    return res.result()        