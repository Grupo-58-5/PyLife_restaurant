from uuid import uuid4
from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from src.restaurants.application.schemas.entry.resaurant_schema_entry import CreateRestaurantSchema
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.restaurants.application.schemas.response.restaurant_schema_response import BaseRestaurantResponse


from src.shared.db.database import get_session

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/", response_model=list[BaseRestaurantResponse])
def get_restaurants(session : Session = Depends(get_session)):
    statement = select(RestaurantModel)
    results = session.exec(statement)
    restaurants =  results.all()
    return [BaseRestaurantResponse(**r.dict()) for r in restaurants]

@router.post("/", response_model=BaseRestaurantResponse, status_code=status.HTTP_201_CREATED)
def create_restaurant(restaurant: CreateRestaurantSchema, session: Session = Depends(get_session)):
    restaurant_id = uuid4()
    restaurant_model = RestaurantModel(
        id=restaurant_id,
        name=restaurant.name,
        location=restaurant.location,
        opening_time=restaurant.opening_time,
        closing_time=restaurant.closing_time
    )
    session.add(restaurant_model)
    session.commit()
    session.refresh(restaurant_model)

    restaurant_response = BaseRestaurantResponse(
        id=restaurant_model.id,
        name=restaurant_model.name,
        location=restaurant_model.location,
        opening_time=restaurant_model.opening_time,
        closing_time=restaurant_model.closing_time
    )
    # Refresh the instance to get the updated state from the database
    return restaurant_response