


from enum import Enum
from uuid import UUID
from pydantic import BaseModel, Field
from typing import Optional
from pydantic.types import UUID4

class MenuCategory(str, Enum):
    """Enumeration for menu categories."""
    Entrada = "Entrada"
    Principal = "Principal"
    Postre = "Postre"
    Bebida = "Bebida"
class CreateMenuItemSchema(BaseModel):
    """Schema for creating a new menu item."""

    name: str = Field(..., description="Name of the menu item", min_length=2)
    description: str = Field(..., description="Description of the menu item", min_length=5)
    category: MenuCategory = Field(..., description="Category of the menu item", min_length=2)
    restaurant_id: UUID | None = Field(
        default=None,
        description="ID of the restaurant to which the menu item belongs"
    )
    
class UpdateMenuSchema(BaseModel): 
    name: Optional[str]= None
    description: Optional[str]= None
    category: Optional[str]= None