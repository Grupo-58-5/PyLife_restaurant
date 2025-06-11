


from uuid import UUID
from pydantic import BaseModel



class MenuItem(BaseModel):
    """Schema for the response of a menu item."""
    id: UUID
    name: str
    description: str
    category: str

class MenuItemBase(BaseModel):
    """Schema for the response of a menu item."""
    id: UUID
    name: str
    description: str
    category: str

class MenuItemResponse(BaseModel):
    """Schema for the response of a menu item."""
    restaurant_id: UUID
    restaurant_name: str
    item: MenuItemBase
