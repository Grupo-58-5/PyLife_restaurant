


from typing import List
from uuid import UUID
from pydantic import BaseModel

from src.restaurants.application.schemas.response.menu_item_response import MenuItemBase


class RestaurantMenuResponse(BaseModel):

    """Schema for the response of a restaurant's menu."""

    restaurant_id: UUID
    restaurant_name: str
    menu: List[MenuItemBase]