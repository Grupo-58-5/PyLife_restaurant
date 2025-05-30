from uuid import uuid4
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from src.restaurants.application.services.create_restaurant_application_service import CreateRestaurantApplicationService
from src.restaurants.application.services.get_all_restaurant_application_sevice import GetAllRestaurantApplicationService
from src.restaurants.infraestructure.repository.restaurant_repository_impl import RestaurantRepositoryImpl
from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse


from src.shared.db.database import get_session

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])

async def get_repository(session: Session = Depends(get_session)) -> RestaurantRepositoryImpl:
    """Get an instance of the RestaurantRepositoryImpl. """
    return RestaurantRepositoryImpl(db=session)

@router.get("/", response_model=list[BaseRestaurantResponse], status_code=status.HTTP_200_OK)
async def get_restaurants(repo : RestaurantRepositoryImpl = Depends(get_repository)):
    try:
        service = GetAllRestaurantApplicationService(repo)
        res= await service.execute()
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

@router.post("/", response_model=BaseRestaurantResponse, status_code=status.HTTP_201_CREATED)
async def create_restaurant(restaurant: CreateRestaurantSchema, repo: RestaurantRepositoryImpl = Depends(get_repository)):
    """
    Create a new restaurant endpoint.
    """
    try:
        service = CreateRestaurantApplicationService(repo)
        res = await service.execute(restaurant)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    