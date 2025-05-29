from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from src.restaurants.infraestructure.model.restaurant_model import RestaurantModel
from src.shared.db.database import get_session

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/", response_model=list[RestaurantModel])
async def get_restaurants(session : Session = Depends(get_session)):
    statement = select(RestaurantModel)
    results = session.exec(statement)
    return results.all()

@router.post("/", response_model=RestaurantModel)
async def create_restaurant(restaurant: RestaurantModel, session: Session = Depends(get_session)):
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant