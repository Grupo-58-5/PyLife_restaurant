


from datetime import time
from typing import List
from uuid import UUID

from pydantic import BaseModel
from src.restaurants.application.schemas.response.table_restaurant_response import BaseTableResponse

from src.restaurants.application.schemas.response.menu_item_response import MenuItemBase, MenuItemResponse


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
    """
    Schema for restaurant response with additional fields.
    
    """
    menu: List[MenuItemBase] = []

    tables: List[BaseTableResponse]

