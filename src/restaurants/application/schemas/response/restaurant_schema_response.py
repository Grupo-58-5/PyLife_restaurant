


from datetime import time
from typing import List
from uuid import UUID

from pydantic import BaseModel
from src.restaurants.application.schemas.response.table_restaurant_response import TableRestaurantResponse


class BaseRestaurantResponse(BaseModel):
    """
    Base schema for restaurant response.
    
    """
    id: UUID
    name: str
    address: str
    opening_hour: time
    closing_hour: time


class RestaurantDetailResponse(BaseRestaurantResponse):
    tables: List[TableRestaurantResponse]
