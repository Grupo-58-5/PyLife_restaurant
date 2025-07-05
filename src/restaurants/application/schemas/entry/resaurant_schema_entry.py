from typing import List
from pydantic import BaseModel, Field
from datetime import time

from src.restaurants.application.schemas.entry.create_table_schema import CreateTableSchema
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

    tables: List[CreateTableSchema] | None = Field(
        default=None,
        description="List of tables in the restaurant. If not provided, no tables will be created.",
    )

    # @field_validator("closing_hour")
    # @classmethod
    # def closing_after_opening(cls, v, info):
    #     """Ensure that closing time is after opening time."""
    #     opening_time = info.data.get("opening_time")
    #     if opening_time is not None and v <= opening_time:
    #         raise ValueError("closing_time must be after opening_time")
    #     return v

class UpdateRestaurantSchema(BaseModel):
    """Schema for updating an existing restaurant entry."""

    name: str | None = Field(default=None)
    address: str | None = Field(default=None, description="Restaurant address.")
    opening_time: time | None = Field(default=time(8, 0), description="Opening time.")
    closing_time: time | None = Field(default=time(12,0), description="Closing time.")

    def validate_schedule(cls, values):
        opening = values.get("opening_time")
        closing = values.get("closing_time")

        if (opening is not None and closing is None) or (closing is not None and opening is None):
            raise ValueError("Both opening_time and closing_time must be provided together.")

        return values
