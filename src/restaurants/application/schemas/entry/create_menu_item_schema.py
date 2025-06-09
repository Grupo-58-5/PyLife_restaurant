


from uuid import UUID
from pydantic import BaseModel, Field


class CreateMenuItemSchema(BaseModel):
    """Schema for creating a new menu item."""

    name: str = Field(..., description="Name of the menu item", min_length=2)
    description: str = Field(..., description="Description of the menu item", min_length=5)
    category: str = Field(..., description="Category of the menu item", min_length=2)