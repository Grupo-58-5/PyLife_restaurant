from typing import List
from pydantic import BaseModel, Field, field_validator
from datetime import time

from src.restaurants.application.schemas.entry.create_menu_item_schema import CreateMenuItemSchema



class CreateRestaurantSchema(BaseModel):
    """Schema for creating a new restaurant entry."""

    name: str = Field(...,
        min_length=3,
        max_length=100,
    )
    address: str = Field(...,
        min_length=3,
        max_length=200,
    )

    opening_hour: time = Field(default=time(8, 0))
    
    closing_hour: time = Field(default=time(22, 0))

    menu_items: List[CreateMenuItemSchema] | None = Field(
        default=None,
        description="List of menu items for the restaurant",
    )


    # @field_validator("closing_hour")
    # @classmethod
    # def closing_after_opening(cls, v, info):
    #     """Ensure that closing time is after opening time."""
    #     opening_time = info.data.get("opening_time")
    #     if opening_time is not None and v <= opening_time:
    #         raise ValueError("closing_time must be after opening_time")
    #     return v